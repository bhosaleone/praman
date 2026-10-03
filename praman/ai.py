"""Praman Deterministic AI Agent Integration (Groq LPU Engine).

Enforces strict mathematical & editorial discipline:
1. PRAMAN MEASURES THE EVIDENCE: AI never touches demand scores, rankings, or autocomplete queries.
2. GROQ STRUCTURES THE EXECUTION: Generates deterministic content briefs, outlines, and FAQ schemas
   strictly grounded in Praman's measured suggestion clusters.
3. 100% Deterministic: Runs at temperature=0.0 and seed=42 with structured JSON outputs.
"""

import json
import logging
import os
from typing import Any, Optional
import urllib.request
from pathlib import Path
import urllib.error

logger = logging.getLogger("praman.ai")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

PRIMARY_MODEL = "openai/gpt-oss-120b"
FALLBACK_MODEL = "qwen/qwen3.8-27b"


def _load_env_file() -> None:
    """Safely loads .env if present without external dependencies."""
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass


_load_env_file()


def get_groq_api_key() -> str:
    """Returns configured Groq API key from environment or local .env."""
    _load_env_file()
    return os.environ.get("GROQ_API_KEY", "").strip()


def _call_groq_chat(
    messages: list[dict[str, str]],
    model: str = PRIMARY_MODEL,
    api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Issues a deterministic chat completion request to Groq."""
    key = (api_key or get_groq_api_key()).strip()
    if not key:
        raise ValueError(
            "Groq API key is not configured. Please enter your free key in the UI or set GROQ_API_KEY."
        )

    payload = {
        "model": model,
        "temperature": 0.0,
        "seed": 42,
        "response_format": {"type": "json_object"},
        "messages": messages,
    }

    req = urllib.request.Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "User-Agent": "Praman/1.0 (Indic Search Intelligence)",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return parsed
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        logger.warning("Groq API error on model %s: %s - %s", model, e, err_body)
        if model != FALLBACK_MODEL:
            logger.info("Retrying with fallback model %s...", FALLBACK_MODEL)
            return _call_groq_chat(messages, model=FALLBACK_MODEL, api_key=api_key)
        raise RuntimeError(f"Groq API error ({e.code}): {err_body or e.reason}")
    except Exception as e:
        logger.exception("Unexpected error in Groq call")
        if model != FALLBACK_MODEL:
            return _call_groq_chat(messages, model=FALLBACK_MODEL, api_key=api_key)
        raise


def generate_editorial_blueprint(
    seed: str,
    language: str = "mr",
    demand: Optional[float] = None,
    intent: str = "informational",
    competition_band: Optional[str] = None,
    suggestions: Optional[list[str]] = None,
    api_key: Optional[str] = None,
) -> dict[str, Any]:
    """Generates a publication-ready editorial blueprint strictly grounded in Praman's data.

    Returns:
    - title: High-CTR SEO title tag
    - meta_description: CTR-optimized meta description (under 160 chars)
    - h1: Primary headline
    - target_word_count: Recommended word budget
    - outline: List of sections with headings, grounded query list, and key points
    - faq: List of { question, answer }
    - faq_schema_jsonld: Ready-to-paste Schema.org/FAQPage JSON-LD
    - markdown_blueprint: Formatted Markdown document
    """
    suggestions = suggestions or []
    demand_str = f"{demand:.3f}" if demand is not None else "unmeasured"
    comp_str = competition_band or "unmeasured"

    system_prompt = (
        "You are Praman's Deterministic Editorial Blueprint Architect for Indic and English publishers. "
        "Transform the provided verified Google search suggestions into a rigorous, production-ready article brief. "
        "\n"
        "STRICT INVARIANTS (NO HALLUCINATIONS):\n"
        "1. All H2/H3 outline headings and FAQs MUST be directly grounded in the provided search queries.\n"
        "2. Do NOT invent facts or fake search volumes.\n"
        "3. Write the title, meta description, outline, and FAQs in the native language corresponding to the seed query.\n"
        "4. Output MUST be valid JSON with keys: title, meta_description, h1, target_word_count, outline, faq.\n"
        "   - outline: array of objects { heading, level ('H2'|'H3'), queries_answered (array of strings), key_points (array of strings) }\n"
        "   - faq: array of objects { question, answer } (2 concise factual sentences each)\n"
    )

    user_context = {
        "seed_keyword": seed,
        "language": language,
        "measured_demand_score": demand_str,
        "search_intent": intent,
        "competition_band": comp_str,
        "verified_google_suggestions": suggestions[:35],
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(user_context, ensure_ascii=False)},
    ]

    parsed = _call_groq_chat(messages, api_key=api_key)

    # Build Schema.org/FAQPage JSON-LD
    faq_items = parsed.get("faq", [])
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item.get("question", item.get("q", "")),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.get("answer", item.get("a", "")),
                },
            }
            for item in faq_items
            if (item.get("question") or item.get("q")) and (item.get("answer") or item.get("a"))
        ],
    }

    # Build Pre-formatted Markdown Blueprint
    title = parsed.get("title", seed)
    meta_desc = parsed.get("meta_description", "")
    h1 = parsed.get("h1", title)
    words = parsed.get("target_word_count", 1200)

    md_lines = [
        f"# {h1}",
        "",
        f"**SEO Title Tag**: {title}  ",
        f"**Meta Description**: {meta_desc}  ",
        f"**Target Word Count**: ~{words} words | **Praman Demand Index**: `{demand_str}` | **Competition**: `{comp_str}` | **Intent**: `{intent}`",
        "",
        "---",
        "",
        "## 📑 Editorial Outline & Section Architecture",
        "",
    ]

    for sec in parsed.get("outline", []):
        lvl = sec.get("level", "H2")
        heading = sec.get("heading", "")
        prefix = "### " if lvl == "H3" else "## "
        md_lines.append(f"{prefix}{heading}")

        queries = sec.get("queries_answered", [])
        if queries:
            md_lines.append(f"*Answering search queries: {', '.join(f'`{q}`' for q in queries)}*")

        points = sec.get("key_points", [])
        for pt in points:
            md_lines.append(f"- {pt}")
        md_lines.append("")

    if faq_items:
        md_lines.append("## ❓ Frequently Asked Questions (PAA & Schema)")
        md_lines.append("")
        for f in faq_items:
            q = f.get("question", f.get("q", ""))
            a = f.get("answer", f.get("a", ""))
            md_lines.append(f"**Q: {q}**  ")
            md_lines.append(f"A: {a}")
            md_lines.append("")

        md_lines.append("### 🏷️ Rank Math / WordPress FAQ Schema (JSON-LD)")
        md_lines.append("```html")
        md_lines.append('<script type="application/ld+json">')
        md_lines.append(json.dumps(faq_schema, indent=2, ensure_ascii=False))
        md_lines.append("</script>")
        md_lines.append("```")

    markdown_blueprint = "\n".join(md_lines)

    return {
        "seed": seed,
        "title": title,
        "meta_description": meta_desc,
        "h1": h1,
        "target_word_count": words,
        "outline": parsed.get("outline", []),
        "faq": faq_items,
        "faq_schema": faq_schema,
        "markdown_blueprint": markdown_blueprint,
        "model_used": PRIMARY_MODEL,
    }


def expand_indic_seeds(
    seed: str,
    source_language: str = "mr",
    api_key: Optional[str] = None,
) -> list[dict[str, str]]:
    """Deterministically expands an Indic seed into culturally authentic search equivalents in other languages."""
    system_prompt = (
        "You are an expert Indic search lexicographer. "
        "Given a seed query in one Indian language or English, return the authentic, colloquial search phrases "
        "that real citizens and farmers type into Google in Hindi, Marathi, and English. "
        "Do NOT do robotic literal translation. Provide exact search query equivalents. "
        "Output MUST be valid JSON with key 'variants': array of objects { language (e.g. 'mr', 'hi', 'en'), seed: string, explanation: string }."
    )

    user_payload = {
        "source_seed": seed,
        "source_language": source_language,
        "target_languages": ["mr", "hi", "en"],
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
    ]

    try:
        parsed = _call_groq_chat(messages, api_key=api_key)
        return parsed.get("variants", [])
    except Exception as e:
        logger.exception("Error expanding seeds via Groq")
        return []
