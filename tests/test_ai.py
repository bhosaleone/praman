"""Tests for praman.ai deterministic Groq integration."""

import json
import unittest
from unittest.mock import MagicMock, patch

from praman.ai import (
    FALLBACK_MODEL,
    PRIMARY_MODEL,
    _call_groq_chat,
    expand_indic_seeds,
    generate_editorial_blueprint,
    get_groq_api_key,
)


class TestPramanAI(unittest.TestCase):
    @patch.dict("os.environ", {"GROQ_API_KEY": "test_dummy_key_12345"})
    def test_get_groq_api_key(self):
        key = get_groq_api_key()
        self.assertEqual(key, "test_dummy_key_12345")

    @patch("urllib.request.urlopen")
    def test_call_groq_chat_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{
                "message": {
                    "content": json.dumps({"title": "Test Title", "outline": []})
                }
            }]
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        messages = [{"role": "user", "content": "hello"}]
        res = _call_groq_chat(messages, model=PRIMARY_MODEL)
        self.assertEqual(res["title"], "Test Title")

    @patch("praman.ai._call_groq_chat")
    def test_generate_editorial_blueprint_structure(self, mock_call):
        mock_call.return_value = {
            "title": "पीक विमा 2026 संपूर्ण माहिती",
            "meta_description": "पीक विमा 2026 बद्दल सर्व माहिती.",
            "h1": "पीक विमा 2026",
            "target_word_count": 1400,
            "outline": [
                {
                    "heading": "पीक विमा अर्ज प्रक्रिया",
                    "level": "H2",
                    "queries_answered": ["पीक विमा अर्ज कसा करावा"],
                    "key_points": ["पोर्टलवर जा", "कागदपत्रे अपलोड करा"]
                }
            ],
            "faq": [
                {
                    "question": "पीक विमा कधी मिळणार?",
                    "answer": "नुकसान भरपाई 30 दिवसांत जमा होते."
                }
            ]
        }

        bp = generate_editorial_blueprint(
            seed="पीक विमा",
            language="mr",
            demand=0.85,
            intent="informational",
            competition_band="low",
            suggestions=["पीक विमा अर्ज कसा करावा"]
        )

        self.assertEqual(bp["seed"], "पीक विमा")
        self.assertEqual(bp["title"], "पीक विमा 2026 संपूर्ण माहिती")
        self.assertIn("H2", bp["outline"][0]["level"])
        self.assertIn("FAQPage", json.dumps(bp["faq_schema"]))
        self.assertIn("# पीक विमा 2026", bp["markdown_blueprint"])

    @patch("praman.ai._call_groq_chat")
    def test_expand_indic_seeds(self, mock_call):
        mock_call.return_value = {
            "variants": [
                {"language": "hi", "seed": "फसल बीमा ऑनलाइन", "explanation": "Hindi query"},
                {"language": "en", "seed": "crop insurance scheme", "explanation": "English query"}
            ]
        }

        variants = expand_indic_seeds("पीक विमा", "mr")
        self.assertEqual(len(variants), 2)
        self.assertEqual(variants[0]["language"], "hi")
        self.assertEqual(variants[1]["language"], "en")


if __name__ == "__main__":
    unittest.main()
