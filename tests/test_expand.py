"""Tests for query expansion and budget accounting."""

import unittest

from praman.expand import (
    create_expansion_plan,
    expand_seed,
    expected_expansion_count,
)


class TestExpansion(unittest.TestCase):
    def test_devanagari_seed_query_count(self):
        # Devanagari seed: 1 (head) + 33 (alphabet) + 8 (modifiers) + 7 (questions) = 49 queries
        exp = expand_seed("मराठी शेती", language_code="mr")
        self.assertEqual(len(exp.queries), 49)
        self.assertEqual(exp.expected_count, 49)
        self.assertTrue(exp.breadth_comparable)

    def test_latin_seed_query_count(self):
        # Latin seed: 1 (head) + 26 (alphabet) + 8 (modifiers) + 7 (questions) = 42 queries
        exp = expand_seed("marathi sheti", language_code="mr")
        self.assertEqual(len(exp.queries), 42)
        self.assertEqual(exp.expected_count, 42)

    def test_construction_order(self):
        """Order must be: head, alphabet, modifiers, questions."""
        exp = expand_seed("शेती", language_code="mr")
        kinds = [q.kind for q in exp.queries]
        self.assertEqual(kinds[0], "head")
        self.assertEqual(kinds[1:34], ["alphabet"] * 33)
        self.assertEqual(kinds[34:42], ["modifier"] * 8)
        self.assertEqual(kinds[42:49], ["question"] * 7)

    def test_query_ceiling_truncation(self):
        # Budget ceiling of 20 cuts off the expansion
        plan = create_expansion_plan(
            seeds=["शेती"],
            language_code="mr",
            max_queries=20,
        )
        self.assertTrue(plan.is_truncated)
        exp = plan.expansions["शेती"]
        self.assertTrue(exp.truncated)
        self.assertFalse(exp.breadth_comparable)
        self.assertEqual(len(exp.queries), 20)
        self.assertEqual(len(exp.not_asked), 29)

    def test_seed_ceiling(self):
        plan = create_expansion_plan(
            seeds=["शेती", "निबंध", "आरोग्य", "हवामान"],
            language_code="mr",
            max_seeds=2,
        )
        self.assertEqual(plan.seeds_used, ["शेती", "निबंध"])
        self.assertEqual(plan.not_asked_seeds, ["आरोग्य", "हवामान"])


if __name__ == "__main__":
    unittest.main()
