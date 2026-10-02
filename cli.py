#!/usr/bin/env python3
"""Praman CLI: Evidence-first Indic keyword demand research & content planning."""

import argparse
from pathlib import Path
import sys

from praman.competition import CompetitionIndex, write_observation_template
from praman.config import Mode, Settings, Weights
from praman.pipeline import run_research
from praman.planner import generate_content_plan
from praman.report import render_csv_report, render_json_report, render_markdown_report


def cmd_research(args: argparse.Namespace) -> int:
    seeds: list[str] = []
    if args.seeds_file:
        with open(args.seeds_file, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    seeds.append(stripped)
    if args.seeds:
        seeds.extend(args.seeds)

    if not seeds:
        print("Error: No seeds provided. Specify seeds as arguments or via --seeds-file.", file=sys.stderr)
        return 1

    settings = Settings(
        language=args.lang,
        region=args.region,
        mode=Mode(args.mode),
        max_seeds=args.max_seeds,
        max_queries=args.max_queries,
        latin_expansion=args.latin_expansion,
        recorded_file=Path(args.recorded) if args.recorded else None,
    )

    comp_idx = None
    if args.serp:
        comp_path = Path(args.serp)
        if comp_path.exists():
            comp_idx = CompetitionIndex.from_csv(comp_path)
        else:
            print(f"Warning: SERP file '{args.serp}' not found; proceeding without competition data.", file=sys.stderr)

    result = run_research(seeds, settings, comp_idx)

    # Format output
    if args.format == "csv":
        output = render_csv_report(result)
    elif args.format == "json":
        output = render_json_report(result, settings.mode)
    else:
        output = render_markdown_report(result, settings.mode)

    if args.out:
        out_p = Path(args.out)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report written to {args.out}")
    else:
        print(output)

    return 0


def cmd_serp(args: argparse.Namespace) -> int:
    seeds: list[str] = []
    if args.seeds_file:
        with open(args.seeds_file, "r", encoding="utf-8") as f:
            seeds.extend([l.strip() for l in f if l.strip() and not l.startswith("#")])
    if args.seeds:
        seeds.extend(args.seeds)

    if not seeds:
        print("Error: No seeds specified for SERP template.", file=sys.stderr)
        return 1

    out_p = Path(args.out)
    try:
        write_observation_template(seeds, out_p, overwrite=args.overwrite)
        print(f"SERP observation template written to {out_p}")
        print("Columns: keyword, top_results_stale, thin_results, weak_domains, own_sites_ranking, notes")
        print("Values: 'yes', 'no', or leave blank for unrecorded.")
    except FileExistsError as e:
        print(f"Error: {e} Use --overwrite to replace existing file.", file=sys.stderr)
        return 1
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    seeds: list[str] = []
    if args.seeds_file:
        with open(args.seeds_file, "r", encoding="utf-8") as f:
            seeds.extend([l.strip() for l in f if l.strip() and not l.startswith("#")])
    if args.seeds:
        seeds.extend(args.seeds)

    if not seeds:
        print("Error: No seeds provided for planning.", file=sys.stderr)
        return 1

    settings = Settings(
        language=args.lang,
        mode=Mode(args.mode),
        recorded_file=Path(args.recorded) if args.recorded else None,
    )

    result = run_research(seeds, settings)
    plan = generate_content_plan(result.scores)

    # Format editorial plan as Markdown
    lines = [
        f"# Praman Editorial Content Plan — Language: {args.lang.upper()}",
        f"Analyzed {len(result.scores)} keywords into {len(plan.clusters)} topic clusters.",
        "",
        "## Recommended Publishing Calendar",
        "| Order | Topic / Title | Cluster Demand | Primary Intent | Recommended Article Shape |",
        "|---|---|---|---|---|",
    ]

    for c in plan.calendar:
        lines.append(
            f"| #{c.recommended_publish_order} | **{c.primary_title}** | {c.cluster_demand:.3f} | `{c.primary_intent}` | {c.article_shape} |"
        )

    lines.extend([
        "",
        "## Internal Link Architecture",
        "| Source Topic | Target Topic | Suggested Anchor Text | Strategic Rationale |",
        "|---|---|---|---|",
    ])

    for link in plan.link_graph:
        lines.append(
            f"| {link.source_topic} | {link.target_topic} | **`{link.anchor_text}`** | {link.rationale} |"
        )

    if plan.orphan_topics:
        lines.extend([
            "",
            "## Standalone / Pillar Topics (No Inbound Links Suggested)",
        ])
        for o in plan.orphan_topics:
            lines.append(f"- `{o}`")

    output = "\n".join(lines)
    if args.out:
        out_p = Path(args.out)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Content plan written to {args.out}")
    else:
        print(output)

    return 0


def cmd_weights(args: argparse.Namespace) -> int:
    w = Weights()
    print("Praman Pinned Demand Voice Weights (MATH.md §6):")
    print(f"  • Breadth (Expansion Breadth):  {w.breadth:.2f} (50%)")
    print(f"  • Coverage (Head Presence):     {w.coverage:.2f} (25%)")
    print(f"  • Density (Question Density):   {w.density:.2f} (15%)")
    print(f"  • Depth (Rank Depth):           {w.depth:.2f} (10%)")
    print("\nInvariants:")
    print("  1. Weights sum strictly to 1.0.")
    print("  2. If any voice is unmeasured, surviving weights do NOT renormalize.")
    print("  3. The score is capped below 1.0 and flagged partial (MATH.md Theorem 2).")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="praman",
        description="Evidence-first keyword demand research and content planning for Indian regional languages.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: research
    p_research = subparsers.add_parser("research", help="Run keyword demand research on seeds")
    p_research.add_argument("seeds", nargs="*", help="Seed keywords to evaluate")
    p_research.add_argument("--seeds-file", help="File with seed keywords (one per line)")
    p_research.add_argument("--lang", default="mr", help="Target language code (e.g. mr, hi, ta, te, bn, gu, kn)")
    p_research.add_argument("--region", default="IN", help="Region code (default: IN)")
    p_research.add_argument("--mode", choices=["fixture", "recorded", "live"], default="fixture", help="Execution mode")
    p_research.add_argument("--recorded", help="Path to recorded.json when mode=recorded")
    p_research.add_argument("--serp", help="Path to human SERP observations CSV")
    p_research.add_argument("--max-seeds", type=int, help="Seed count ceiling")
    p_research.add_argument("--max-queries", type=int, help="Total query count ceiling")
    p_research.add_argument("--latin-expansion", action="store_true", help="Include A-Z alphabet expansion")
    p_research.add_argument("--format", choices=["md", "csv", "json"], default="md", help="Output format")
    p_research.add_argument("-o", "--out", help="Output file path")
    p_research.set_defaults(func=cmd_research)

    # Subcommand: serp
    p_serp = subparsers.add_parser("serp", help="Generate human SERP observation template CSV")
    p_serp.add_argument("seeds", nargs="*", help="Seed keywords")
    p_serp.add_argument("--seeds-file", help="File with seed keywords")
    p_serp.add_argument("-o", "--out", required=True, help="Output CSV path")
    p_serp.add_argument("--overwrite", action="store_true", help="Overwrite if output file exists")
    p_serp.set_defaults(func=cmd_serp)

    # Subcommand: plan
    p_plan = subparsers.add_parser("plan", help="Generate editorial publishing calendar and link graph")
    p_plan.add_argument("seeds", nargs="*", help="Seed keywords")
    p_plan.add_argument("--seeds-file", help="File with seed keywords")
    p_plan.add_argument("--lang", default="mr", help="Target language code")
    p_plan.add_argument("--mode", choices=["fixture", "recorded", "live"], default="fixture", help="Execution mode")
    p_plan.add_argument("--recorded", help="Path to recorded.json")
    p_plan.add_argument("-o", "--out", help="Output markdown file path")
    p_plan.set_defaults(func=cmd_plan)

    # Subcommand: weights
    p_weights = subparsers.add_parser("weights", help="Display pinned demand weights and algebraic rules")
    p_weights.set_defaults(func=cmd_weights)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
