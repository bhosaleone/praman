"""Tests for topic clustering and editorial content planning."""

import unittest

from praman.intent import IntentResult
from praman.planner import cluster_keywords, generate_content_plan
from praman.scoring import KeywordScore
from praman.signals import SeedSignals


class TestPlanner(unittest.TestCase):
    def _make_score(self, seed: str, demand: float, intent: str = "informational") -> KeywordScore:
        sig = SeedSignals(
            seed=seed,
            coverage=1.0,
            breadth=demand,
            depth=1.0,
            density=0.0,
            best_rank=1,
            suggestions_seen=10,
            cross_script_split={},
            script_affinity=1.0,
            axis_yield={},
            discovered=[],
            breadth_comparable=True,
            queries_asked=49,
            queries_measured=49,
            queries_absent=0,
            queries_failed=0,
        )
        return KeywordScore(
            seed=seed,
            demand=demand,
            demand_complete=True,
            measured_mass=1.0,
            raw_axes={},
            components={},
            unmeasured_voices=[],
            intent=IntentResult(intent=intent, markers_matched=[], article_shape="Guide", is_question=False),
            competition=None,
            priority_band="high",
            signals=sig,
        )

    def test_clustering_bilingual_topics(self):
        """Cross-script spellings 'मराठी शेती' and 'marathi sheti' must group into ONE topic cluster."""
        k1 = self._make_score("मराठी शेती", 0.65)
        k2 = self._make_score("marathi sheti", 0.52)
        k3 = self._make_score("आरोग्य माहिती", 0.40)

        clusters = cluster_keywords([k1, k2, k3])
        self.assertEqual(len(clusters), 2)

        # Cluster 1 must contain both Marathi Sheti spellings
        c1 = [c for c in clusters if "शेती" in c.primary_title or "sheti" in c.primary_title][0]
        self.assertEqual(len(c1.keywords), 2)
        self.assertEqual(c1.primary_title, "मराठी शेती")  # Higher demand wins title

    def test_content_plan_calendar_and_links(self):
        k1 = self._make_score("मराठी शेती", 0.70, intent="informational")
        k2 = self._make_score("शेती कशी करावी", 0.50, intent="howto")
        k3 = self._make_score("शेती योजना 2026", 0.45, intent="freshness")

        plan = generate_content_plan([k1, k2, k3])
        self.assertEqual(len(plan.calendar), 3)
        self.assertEqual(plan.calendar[0].primary_title, "मराठी शेती")
        self.assertTrue(len(plan.link_graph) > 0)


if __name__ == "__main__":
    unittest.main()
