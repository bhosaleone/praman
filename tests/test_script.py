"""Tests for Indic script handling and linguistic boundary detection."""

import unittest

from praman.script import (
    dedup_key,
    fold,
    script_of,
    sibling_key,
    tokenize,
    topic_key,
    word_boundary_regex,
)


class TestScriptProcessing(unittest.TestCase):
    def test_script_detection(self):
        self.assertEqual(script_of("मराठी शेती"), "devanagari")
        self.assertEqual(script_of("தமிழ் சினிமா"), "tamil")
        self.assertEqual(script_of("తెలుగు వార్తలు"), "telugu")
        self.assertEqual(script_of("marathi sheti"), "latin")
        self.assertEqual(script_of("मराठी board paper"), "mixed")

    def test_combining_marks_word_boundary(self):
        """Verifies that Brahmic combining marks (matras) do NOT trigger false regex word boundaries."""
        # Standard \b would match inside 'किती' because 'ि' is a combining mark
        pattern = word_boundary_regex("किती")

        # Must match standalone word
        self.assertTrue(pattern.search("हा खर्च किती आहे"))
        self.assertTrue(pattern.search("किती?"))

        # Must NOT match inside an inflected form like 'कितीचा' or 'कितीत'
        self.assertIsNone(pattern.search("त्या कितीचा हिशोब"))
        self.assertIsNone(pattern.search("यात कितितरा फरक"))

    def test_folding_and_dedup(self):
        # Strips zero-width characters and normalizes whitespace
        s1 = "मराठी\u200c शेती"
        s2 = "  मराठी    शेती  "
        self.assertEqual(fold(s1), "मराठी शेती")
        self.assertEqual(dedup_key(s1), dedup_key(s2))

    def test_topic_key_consonant_skeleton(self):
        """Cross-script identity: 'मराठी शेती' and 'marathi sheti' should produce identical topic_key."""
        k_dev = topic_key("मराठी शेती")
        k_lat = topic_key("marathi sheti")
        self.assertEqual(k_dev, k_lat)
        self.assertEqual(k_dev, "mrtst")

    def test_tokenize(self):
        tokens = tokenize("शेती विषयक ताज्या बातम्या 2026!")
        self.assertIn("शेती", tokens)
        self.assertIn("ताज्या", tokens)
        self.assertIn("2026", tokens)


if __name__ == "__main__":
    unittest.main()
