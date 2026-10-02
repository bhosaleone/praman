"""Unit tests verifying candidate quality filtering and English language expansion."""

import unittest

from praman.autocomplete import AutocompleteResult
from praman.expand import ExpansionQuery, expand_seed
from praman.languages import get_language_spec
from praman.signals import calculate_seed_signals


class TestCandidateFilterAndEnglish(unittest.TestCase):
    def test_candidate_quality_filter_separates_artifacts(self):
        """Verifies that alphabet probes like 'पीक विमा क' stay in raw observations,
        while 'पीक विमा 2026' and 'पीक विमा किती' pass to research candidates."""
        seed = "पीक विमा"
        queries = [ExpansionQuery(query=seed, seed=seed, kind="head", tag="")]
        
        raw_strings = [
            "पीक विमा क",               # Alphabet artifact (trailing single letter)
            "पीक विमा क 2026",          # Alphabet artifact (isolated middle probe)
            "पीक विमा 2026",            # Clean candidate
            "पीक विमा online",          # Clean candidate
            "पीक विमा किती",            # Clean candidate
            "marathi sheti a",          # Alphabet artifact
            "marathi sheti guide",      # Clean candidate
        ]
        
        results = {
            seed: AutocompleteResult(
                query=seed,
                suggestions=tuple(raw_strings),
                measured=True,
                source="fixture",
            )
        }
        
        signals = calculate_seed_signals(
            seed=seed,
            queries=queries,
            results=results,
            all_seeds=[seed],
            breadth_comparable=True,
            language_code="mr",
        )
        
        # All 7 strings should be in raw_observations
        for s in raw_strings:
            self.assertIn(s, signals.raw_observations)
        
        # Artifacts should NOT be in research_candidates
        self.assertNotIn("पीक विमा क", signals.research_candidates)
        self.assertNotIn("पीक विमा क 2026", signals.research_candidates)
        self.assertNotIn("marathi sheti a", signals.research_candidates)
        
        # Genuine candidates MUST be in research_candidates
        self.assertIn("पीक विमा 2026", signals.research_candidates)
        self.assertIn("पीक विमा online", signals.research_candidates)
        self.assertIn("पीक विमा किती", signals.research_candidates)
        self.assertIn("marathi sheti guide", signals.research_candidates)

    def test_english_language_config_and_expansion(self):
        """Verifies English language config has Latin alphabet and interrogatives, and expands seeds cleanly."""
        en_cfg = get_language_spec("en")
        self.assertIsNotNone(en_cfg)
        self.assertEqual(en_cfg.name, "English")
        self.assertTrue(any("how to" in t for t in en_cfg.question_templates))
        self.assertTrue(any("what is" in t for t in en_cfg.question_templates))
        self.assertTrue(any("guide" == m[0] for m in en_cfg.modifier_templates))
        
        # Expand an English seed
        expansions = expand_seed("organic farming", language_code="en")
        queries = [e.query for e in expansions.queries]
        
        # Head query
        self.assertIn("organic farming", queries)
        # Alphabet expansion
        self.assertIn("organic farming a", queries)
        self.assertIn("organic farming b", queries)
        # Modifier expansion
        self.assertTrue(any("guide" in q for q in queries))
        # Question expansion (SVO: interrogative at start)
        self.assertTrue(any(q.startswith("what") or q.startswith("how") for q in queries))


if __name__ == "__main__":
    unittest.main()
