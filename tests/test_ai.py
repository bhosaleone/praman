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

    def test_audit_blueprint_quality(self):
        from praman.ai import audit_blueprint_quality

        sample_data = {
            "title": "बॅटरी स्प्रे पंप 2026 किंमत व मार्गदर्शक",
            "meta_description": "2026 मधील सर्वोत्तम बॅटरी स्प्रे पंप किंमत ₹3500 ते ₹5000.",
            "h1": "बॅटरी स्प्रे पंप संपूर्ण माहिती 2026",
            "paisa_vasool_criteria": ["12V 12Ah बॅटरी बॅकअप", "ब्रास नोझल टिकाऊपणा"],
            "verification_checklist": ["होलोग्राम तपासा", "जीएसटी बिल घ्या"],
            "subsidy_eligibility": "MahaDBT 50% कृषी अनुदान योजना",
            "outline": [
                {
                    "heading": "बॅटरी स्प्रे पंप किंमत व बजेट 2026",
                    "level": "H2",
                    "queries_answered": ["बॅटरी स्प्रे पंप किंमत"],
                    "key_points": ["किंमत ₹3,500 ते ₹5,000", "12V 12Ah बॅटरी क्षमता 5 तास"]
                },
                {
                    "heading": "महाडीबीटी अनुदान अर्ज पद्धत",
                    "level": "H2",
                    "queries_answered": ["बॅटरी स्प्रे पंप अनुदान"],
                    "key_points": ["mahadbt.maharashtra.gov.in पोर्टलवर अर्ज करा", "7/12 उतारा आवश्यक"]
                }
            ],
            "faq": [
                {"question": "बॅटरी स्प्रे पंप किंमत काय आहे?", "answer": "बाजारात सरासरी ₹3,500 ते ₹5,200 किंमत असते."},
                {"question": "अनुदान कसे मिळते?", "answer": "महाडीबीटी पोर्टलवर ऑनलाईन अर्ज करावा लागतो."}
            ],
            "product_review_schema": {
                "name": "बॅटरी स्प्रे पंप",
                "rating": 4.6,
                "price_bracket": "₹3,500 - ₹5,000",
                "pros": ["चांगला बॅकअप"],
                "cons": ["वजन जास्त"]
            }
        }

        audit = audit_blueprint_quality(
            blueprint_data=sample_data,
            suggestions=["बॅटरी स्प्रे पंप किंमत", "बॅटरी स्प्रे पंप अनुदान", "बॅटरी स्प्रे पंप 12v"],
            effective_intent="commercial",
            language="mr"
        )

        self.assertGreaterEqual(audit["overall_score"], 85)
        self.assertIn("A", audit["grade"])
        self.assertEqual(audit["intent_score"], 25)
        self.assertIn("₹ INR Pricing & Value Brackets", audit["metrics_detected"])
        self.assertIn("Technical Units & Capacity (V/Ah/HP/L/%)", audit["metrics_detected"])
        self.assertIn("Official Portals & Verification Markers", audit["metrics_detected"])
        self.assertIn("Zero Generic AI Filler Phrases", audit["metrics_detected"])
        self.assertGreaterEqual(len(audit["audit_checks"]), 5)

    @patch("praman.ai._call_groq_chat")
    def test_generate_howto_blueprint(self, mock_call):
        mock_call.return_value = {
            "title": "पीक विमा अर्ज कसा करावा: 2026 संपूर्ण पद्धत",
            "meta_description": "पीक विमा 2026 ऑनलाईन फॉर्म कसा भरावा.",
            "h1": "पीक विमा ऑनलाईन अर्ज पद्धत 2026",
            "target_word_count": 1600,
            "prerequisites_and_documents": ["7/12 उतारा", "आधार कार्ड", "बँक पासबुक"],
            "rejection_pitfalls": ["चुकीचा बँक खाते क्रमांक", "अपूर्ण स्वाक्षरी"],
            "outline": [
                {
                    "heading": "पात्रता व लागणारी कागदपत्रे",
                    "level": "H2",
                    "queries_answered": ["पीक विमा कागदपत्रे"],
                    "key_points": ["7/12 व आधार लिंक असणे गरजेचे आहे"]
                },
                {
                    "heading": "ऑनलाईन अर्ज करण्याची पायरी-पायरी पद्धत",
                    "level": "H2",
                    "queries_answered": ["पीक विमा अर्ज कसा करावा"],
                    "key_points": ["pmfby.gov.in वर नोंदणी करा", "कागदपत्रे अपलोड करा"]
                }
            ],
            "faq": [
                {"question": "अर्जाची अंतिम तारीख काय आहे?", "answer": "31 जुलै 2026 पर्यंत मुदत असते."}
            ],
            "howto_schema": {
                "name": "पीक विमा अर्ज",
                "total_time": "PT15M",
                "steps": [
                    {"name": "पोर्टल नोंदणी", "text": "पोर्टलवर जाऊन नोंदणी करा."},
                    {"name": "फॉर्म भरणे", "text": "तपशील भरा व सबमिट करा."}
                ]
            }
        }

        bp = generate_editorial_blueprint(
            seed="पीक विमा अर्ज कसा करावा",
            language="mr",
            demand=0.72,
            intent="howto",
            competition_band="low",
            suggestions=["पीक विमा अर्ज कसा करावा", "पीक विमा कागदपत्रे"],
            blueprint_type="howto"
        )

        self.assertEqual(bp["effective_intent"], "howto")
        self.assertIsNotNone(bp["howto_schema"])
        self.assertIn("HowTo", json.dumps(bp["howto_schema"]))
        self.assertIn("पात्रता व आवश्यक कागदपत्रे", bp["markdown_blueprint"])
        self.assertIn("Rejection Pitfalls", bp["markdown_blueprint"])
        self.assertIn("Qualitative Consistency", bp["markdown_blueprint"])


if __name__ == "__main__":
    unittest.main()
