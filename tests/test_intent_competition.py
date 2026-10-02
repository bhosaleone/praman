"""Tests for search intent classification and SERP competition parsing."""

import tempfile
from pathlib import Path
import unittest

from praman.competition import (
    CompetitionIndex,
    derive_competition_band,
    write_observation_template,
)
from praman.intent import classify_intent, looks_like_question


class TestIntentAndCompetition(unittest.TestCase):
    def test_intent_ladder_precedence(self):
        """Transactional markers must win over informational markers."""
        res = classify_intent("शेती योजना pdf माहिती", language_code="mr")
        self.assertEqual(res.intent, "transactional")
        self.assertIn("pdf", res.markers_matched)

    def test_unclear_when_no_markers(self):
        """Never defaults to informational; unmarked queries become 'unclear'."""
        res = classify_intent("केळी", language_code="mr")
        self.assertEqual(res.intent, "unclear")
        self.assertEqual(len(res.markers_matched), 0)

    def test_question_detection(self):
        self.assertTrue(looks_like_question("शेती कशी करावी", language_code="mr"))
        self.assertTrue(looks_like_question("sheti kashi karavi", language_code="mr"))
        self.assertFalse(looks_like_question("शेती अवजारे", language_code="mr"))

    def test_competition_band_derivation(self):
        # < 2 fields recorded yields None (unmeasured)
        band, count = derive_competition_band(thin=True, weak=None, stale=None)
        self.assertIsNone(band)
        self.assertEqual(count, 1)

        # >= 2 fields: weak=True and thin=True -> low
        band, count = derive_competition_band(thin=True, weak=True, stale=None)
        self.assertEqual(band, "low")
        self.assertEqual(count, 2)

        # weak=False and thin=False -> very_high
        band, count = derive_competition_band(thin=False, weak=False, stale=False)
        self.assertEqual(band, "very_high")
        self.assertEqual(count, 3)

    def test_serp_csv_parsing_and_lookup(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write("keyword,top_results_stale,thin_results,weak_domains,own_sites_ranking,notes\n")
            f.write("मराठी शेती,yes,yes,yes,no,weak forum threads ranking\n")
            f.write("शेती योजना,,,no,,\n")  # Only 1 field recorded
            tmp_path = Path(f.name)

        try:
            idx = CompetitionIndex.from_csv(tmp_path)
            obs1 = idx.lookup("मराठी शेती")
            self.assertIsNotNone(obs1)
            self.assertEqual(obs1.band, "low")

            # Topic key fallback: 'marathi sheti' should match 'मराठी शेती' note
            obs_fallback = idx.lookup("marathi sheti")
            self.assertIsNotNone(obs_fallback)
            self.assertEqual(obs_fallback.band, "low")

            # < 2 fields recorded has band None
            obs2 = idx.lookup("शेती योजना")
            self.assertIsNotNone(obs2)
            self.assertIsNone(obs2.band)
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
