"""Tests verifying mathematical theorems and bounds in MATH.md §6."""

import unittest

from praman.config import Weights
from praman.intent import IntentResult
from praman.scoring import score_seed
from praman.signals import SeedSignals


class TestMathematicalScoring(unittest.TestCase):
    def _dummy_signals(
        self,
        breadth: float | None = 0.50,
        coverage: float | None = 1.00,
        density: float | None = 0.20,
        depth: float | None = 1.00,
    ) -> SeedSignals:
        return SeedSignals(
            seed="परीक्षण",
            coverage=coverage,
            breadth=breadth,
            depth=depth,
            density=density,
            best_rank=1 if depth else None,
            suggestions_seen=10,
            cross_script_split={"devanagari": 10, "latin": 0, "mixed": 0, "other": 0},
            script_affinity=1.0,
            axis_yield={},
            discovered=[],
            breadth_comparable=True,
            queries_asked=49,
            queries_measured=49,
            queries_absent=0,
            queries_failed=0,
        )

    def _dummy_intent(self) -> IntentResult:
        return IntentResult(
            intent="informational",
            markers_matched=[],
            article_shape="Explainer",
            is_question=False,
        )

    def test_full_measurement_theorem1(self):
        """When all voices are measured (c = 1.0), lo <= demand <= hi <= 1.0."""
        sig = self._dummy_signals(breadth=0.40, coverage=1.00, density=0.20, depth=0.80)
        score = score_seed(sig, self._dummy_intent())

        self.assertTrue(score.demand_complete)
        self.assertAlmostEqual(score.measured_mass, 1.0)

        # Expected: 0.50*0.40 + 0.25*1.00 + 0.15*0.20 + 0.10*0.80
        # = 0.20 + 0.25 + 0.03 + 0.08 = 0.56
        self.assertAlmostEqual(score.demand, 0.56)

        # Theorem 1 bounds: lo=0.20, hi=1.00
        self.assertTrue(0.20 <= score.demand <= 1.00)

    def test_partial_measurement_theorem2(self):
        """When a voice is unmeasured (e.g. depth=None), c(s) < 1.0 and demand_complete=False."""
        sig = self._dummy_signals(breadth=0.40, coverage=1.00, density=0.20, depth=None)
        score = score_seed(sig, self._dummy_intent())

        self.assertFalse(score.demand_complete)
        # Measured mass without depth (0.10) is 0.90
        self.assertAlmostEqual(score.measured_mass, 0.90)

        # Expected: 0.50*0.40 + 0.25*1.00 + 0.15*0.20 = 0.20 + 0.25 + 0.03 = 0.48
        self.assertAlmostEqual(score.demand, 0.48)
        self.assertIn("depth", score.unmeasured_voices)

    def test_no_silent_renormalization(self):
        """CRITICAL INVARIANT: Weights must NEVER renormalize to survivors when a voice is unmeasured."""
        # Only coverage measured (1.0), others None
        sig = self._dummy_signals(breadth=None, coverage=1.00, density=None, depth=None)
        score = score_seed(sig, self._dummy_intent())

        # NOMINAL weight of coverage is 0.25. If renormalized, it would be 1.0.
        # It MUST remain 0.25!
        self.assertAlmostEqual(score.demand, 0.25)
        self.assertFalse(score.demand_complete)
        self.assertAlmostEqual(score.measured_mass, 0.25)

    def test_all_unmeasured_yields_none(self):
        """If all voices failed/unmeasured, demand is None, NEVER 0.0."""
        sig = self._dummy_signals(breadth=None, coverage=None, density=None, depth=None)
        score = score_seed(sig, self._dummy_intent())

        self.assertIsNone(score.demand)
        self.assertFalse(score.demand_complete)
        self.assertEqual(score.priority_band, "needs-measurement")
        self.assertEqual(score.evidence_band, "insufficient")

    def test_evidence_band_calibration(self):
        """Calibrates evidence bands: Strong (>=0.50), Moderate (>=0.25), Weak (<0.25), Insufficient (None)."""
        # Strong
        s_strong = score_seed(self._dummy_signals(breadth=0.80, coverage=1.00, density=0.20, depth=1.00), self._dummy_intent())
        self.assertEqual(s_strong.evidence_band, "strong")

        # Moderate
        s_mod = score_seed(self._dummy_signals(breadth=0.30, coverage=0.50, density=0.00, depth=0.00), self._dummy_intent())
        # 0.50*0.30 + 0.25*0.50 = 0.15 + 0.125 = 0.275
        self.assertEqual(s_mod.evidence_band, "moderate")

        # Weak
        s_weak = score_seed(self._dummy_signals(breadth=0.10, coverage=0.20, density=0.00, depth=0.00), self._dummy_intent())
        # 0.50*0.10 + 0.25*0.20 = 0.05 + 0.05 = 0.10
        self.assertEqual(s_weak.evidence_band, "weak")

        # Insufficient
        s_none = score_seed(self._dummy_signals(breadth=None, coverage=None, density=None, depth=None), self._dummy_intent())
        self.assertEqual(s_none.evidence_band, "insufficient")


if __name__ == "__main__":
    unittest.main()
