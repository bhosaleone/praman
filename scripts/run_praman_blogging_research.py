#!/usr/bin/env python3
"""Run real research on Blogging in India using Praman's actual pipeline."""

import json
from praman.config import Mode, Settings
from praman.pipeline import run_research

def research_language(seeds, lang, region="IN"):
    settings = Settings(
        language=lang,
        region=region,
        mode=Mode.LIVE,
        latin_expansion=True,
        max_queries=150
    )
    print(f"\n=======================================================")
    print(f"RUNNING PRAMAN RESEARCH FOR [{lang.upper()}] SEEDS: {seeds}")
    print(f"=======================================================")
    
    result = run_research(seeds, settings)
    
    data = []
    for s in result.scores:
        demand_val = f"{s.demand:.4f}" if s.demand is not None else "⊥ (Unmeasured)"
        print(f"\nSeed: {s.seed}")
        print(f"  Demand Score: {demand_val} (Band: {s.evidence_band})")
        print(f"  Intent: {s.intent.intent} | Shape: {s.intent.article_shape}")
        print(f"  Breadth: {s.signals.breadth if s.signals.breadth is not None else '⊥'}")
        print(f"  Head Coverage: {s.signals.coverage if s.signals.coverage is not None else '⊥'}")
        print(f"  Question Density: {s.signals.density if s.signals.density is not None else '⊥'}")
        print(f"  Total Suggestions Seen: {s.signals.suggestions_seen}")
        
        sample_suggs = s.signals.discovered[:20]
        print(f"  Discovered Candidate Keywords ({len(sample_suggs)}):")
        for sug in sample_suggs[:10]:
            print(f"    - {sug}")
            
        data.append({
            "seed": s.seed,
            "language": lang,
            "demand": s.demand,
            "evidence_band": s.evidence_band,
            "intent": s.intent.intent,
            "signals": {
                "breadth": s.signals.breadth,
                "coverage": s.signals.coverage,
                "density": s.signals.density,
                "depth": s.signals.depth,
                "suggestions_seen": s.signals.suggestions_seen,
            },
            "discovered_keywords": s.signals.discovered
        })
    return data

if __name__ == "__main__":
    all_data = {}
    
    # 1. Marathi Blogging Seeds
    all_data["marathi"] = research_language(
        ["ब्लॉग कसा सुरू करावा", "ब्लॉग मधून पैसे", "मराठी ब्लॉगिंग"],
        "mr"
    )
    
    # 2. Hindi Blogging Seeds
    all_data["hindi"] = research_language(
        ["ब्लॉगिंग कैसे शुरू करें", "ब्लॉग से पैसे कैसे कमाए", "ब्लॉगिंग नीच आइडियाज"],
        "hi"
    )
    
    # 3. English Indic Blogging Seeds
    all_data["english"] = research_language(
        ["blogging in India", "how to start a blog in India", "regional language blogging"],
        "en"
    )
    
    with open("scripts/blogging_research_results.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
        
    print("\n[SUCCESS] Research complete! Saved to scripts/blogging_research_results.json")
