"""Tests for Indian affiliate marketer features, commercial intent probing, and Paisa-Vasool blueprints."""

import json
import unittest
from unittest.mock import patch

from praman.ai import generate_editorial_blueprint
from praman.autocomplete import AutocompleteResult
from praman.config import Settings
from praman.expand import expand_seed, expected_expansion_count
from praman.languages import (
    COMMERCIAL_AFFILIATE_MODIFIERS,
    detect_buyer_intent,
    get_commercial_modifiers,
)
from praman.signals import calculate_seed_signals


class TestIndianAffiliateFeatures(unittest.TestCase):
    def test_commercial_modifiers_presence(self):
        """Marathi, Hindi, and English must have defined Indian commercial modifiers."""
        mr_mods = get_commercial_modifiers("mr")
        self.assertGreaterEqual(len(mr_mods), 8)
        mod_texts = [m[0] for m in mr_mods]
        self.assertIn("किंमत", mod_texts)
        self.assertIn("अनुदान", mod_texts)
        self.assertIn("खरे की खोटे", mod_texts)
        self.assertIn("वॉरंटी", mod_texts)

        hi_mods = get_commercial_modifiers("hi")
        self.assertGreaterEqual(len(hi_mods), 8)
        hi_texts = [m[0] for m in hi_mods]
        self.assertIn("कीमत", hi_texts)
        self.assertIn("सब्सिडी", hi_texts)
        self.assertIn("असली या नकली", hi_texts)

        en_mods = get_commercial_modifiers("en")
        self.assertGreaterEqual(len(en_mods), 8)
        en_texts = [m[0] for m in en_mods]
        self.assertIn("subsidy", en_texts)
        self.assertIn("original vs fake", en_texts)

    def test_detect_buyer_intent(self):
        """detect_buyer_intent must identify the core Indian buying dimensions."""
        # Price & Paisa Vasool
        self.assertEqual(detect_buyer_intent("बॅटरी स्प्रे पंप किंमत"), "price")
        self.assertEqual(detect_buyer_intent("solar panel price 2026"), "price")
        self.assertEqual(detect_buyer_intent("ट्रॅक्टर दर काय आहे"), "price")

        # Trust Deficit (Real vs Fake / Complaints / Helpline)
        self.assertEqual(detect_buyer_intent("बलवान स्प्रे पंप खरे की खोटे"), "trust")
        self.assertEqual(detect_buyer_intent("रेडमी फोन असली या नकली पहचान"), "trust")
        self.assertEqual(detect_buyer_intent("टाटा सोलर कस्टमर केअर नंबर"), "trust")
        self.assertEqual(detect_buyer_intent("कंपनी तक्रार नंबर"), "trust")

        # Sarkari Anudan (Subsidies & DBT)
        self.assertEqual(detect_buyer_intent("ठिबक सिंचन अनुदान महाराष्ट्र"), "subsidy")
        self.assertEqual(detect_buyer_intent("पीएम सूर्य घर योजना सब्सिडी"), "subsidy")
        self.assertEqual(detect_buyer_intent("mahadbt tractor yojana 2026"), "subsidy")

        # Head-to-Head Comparison
        self.assertEqual(detect_buyer_intent("balwan vs kisankraft spray pump"), "comparison")
        self.assertEqual(detect_buyer_intent("सोलर इन्व्हर्टर तुलना"), "comparison")

        # Warranty & Durability
        self.assertEqual(detect_buyer_intent("सोलर पॅनल वॉरंटी क्लेम"), "warranty")
        self.assertEqual(detect_buyer_intent("स्प्रेअर स्पेअर पार्ट्स"), "warranty")

        # Budget Brackets
        self.assertEqual(detect_buyer_intent("10000 च्या आत बेस्ट मोबाईल"), "budget")
        self.assertEqual(detect_buyer_intent("phone under 15000 5g"), "budget")

        # Non-commercial query returns None
        self.assertIsNone(detect_buyer_intent("हवामान अंदाज आजचा"))

    def test_commercial_expansion_counts(self):
        """When commercial_expansion=False, count is 49; when True, commercial probes are added."""
        # Baseline Marathi Devanagari: 1 + 33 + 8 + 7 = 49
        exp_baseline = expand_seed("बॅटरी स्प्रे पंप", language_code="mr", commercial_expansion=False)
        self.assertEqual(len(exp_baseline.queries), 49)
        self.assertEqual(exp_baseline.expected_count, 49)

        # With Indian Commercial Probing: 49 + 10 commercial modifiers = 59
        exp_commercial = expand_seed("बॅटरी स्प्रे पंप", language_code="mr", commercial_expansion=True)
        mr_mod_count = len(get_commercial_modifiers("mr"))
        self.assertEqual(len(exp_commercial.queries), 49 + mr_mod_count)
        self.assertEqual(exp_commercial.expected_count, 49 + mr_mod_count)

        # Commercial queries must have kind='commercial'
        commercial_queries = [q for q in exp_commercial.queries if q.kind == "commercial"]
        self.assertEqual(len(commercial_queries), mr_mod_count)
        self.assertTrue(any(q.query.endswith("किंमत") for q in commercial_queries))
        self.assertTrue(any(q.query.endswith("अनुदान") for q in commercial_queries))
        self.assertTrue(any(q.query.endswith("खरे की खोटे") for q in commercial_queries))

    def test_buyer_intent_score_calculation(self):
        """SeedSignals must calculate commercial intent density and matched aspects."""
        seed = "बॅटरी स्प्रे पंप"
        exp = expand_seed(seed, language_code="mr")

        # Synthetic results with commercial suggestions
        results = {
            seed: AutocompleteResult(
                query=seed,
                suggestions=(
                    "बॅटरी स्प्रे पंप किंमत",
                    "बॅटरी स्प्रे पंप अनुदान योजना",
                    "बॅटरी स्प्रे पंप कसा वापरायचा",
                    "बॅटरी स्प्रे पंप वॉरंटी",
                    "बॅटरी स्प्रे पंप माहिती",
                ),
                measured=True,
                source="fixture",
            )
        }

        signals = calculate_seed_signals(
            seed=seed,
            queries=exp.queries,
            results=results,
            all_seeds=[seed],
            breadth_comparable=True,
            language_code="mr",
        )

        # 3 out of 5 suggestions have commercial tokens (किंमत -> price, अनुदान -> subsidy, वॉरंटी -> warranty)
        self.assertIsNotNone(signals.buyer_intent_score)
        self.assertGreater(signals.buyer_intent_score, 0.4)
        self.assertIn("price", signals.buyer_intent_aspects)
        self.assertIn("subsidy", signals.buyer_intent_aspects)
        self.assertIn("warranty", signals.buyer_intent_aspects)

    @patch("praman.ai._call_groq_chat")
    def test_paisa_vasool_affiliate_blueprint(self, mock_groq):
        """generate_editorial_blueprint in affiliate mode must produce Paisa-Vasool and Review schemas."""
        mock_groq.return_value = {
            "title": "सर्वोत्कृष्ट बॅटरी स्प्रे पंप 2026: किंमत, अनुदान व अस्सल रिव्ह्यू",
            "meta_description": "2026 मधील सर्वोत्तम बॅटरी स्प्रे पंप, महाडीबीटी अनुदान आणि अस्सल ओळखण्याची पद्धत.",
            "h1": "बॅटरी स्प्रे पंप संपूर्ण खरेदी मार्गदर्शक 2026",
            "target_word_count": 1800,
            "paisa_vasool_criteria": [
                "12V 12Ah बॅटरी क्षमता (एकदा चार्ज केल्यावर 25-30 पंप फवारणी)",
                "डबल मोटर प्रेशर आणि ब्रास गन टिकाऊपणा",
                "स्थानिक बाजारात स्पेअर पार्ट्स आणि बॅटरी उपलब्धता",
            ],
            "verification_checklist": [
                "कंपनीचा 3D होलोग्राम स्टीकर तपासा",
                "मोटर आणि बॅटरीवरील ISI मार्क आणि सिरीयल नंबर जुळवा",
                "अधिकृत डीलरचे जीएसटी बिल घ्या",
            ],
            "subsidy_eligibility": [
                "MahaDBT शेतकरी योजना: कृषी यांत्रिकीकरण अंतर्गत 50% अनुदान",
                "आवश्यक कागदपत्रे: 7/12 उतारा, 8-अ, आधार कार्ड, बँक पासबुक",
            ],
            "outline": [
                {
                    "heading": "सर्वोत्कृष्ट 3 बॅटरी स्प्रे पंप तुलना",
                    "level": "H2",
                    "queries_answered": ["बॅटरी स्प्रे पंप तुलना", "बॅटरी स्प्रे पंप vs"],
                    "key_points": ["बलवान 12V vs किसानक्राफ्ट", "वॉरंटी आणि बॅटरी बॅकअप"],
                }
            ],
            "faq": [
                {
                    "question": "बॅटरी स्प्रे पंपवर किती अनुदान मिळते?",
                    "answer": "महाडीबीटी योजनेतून सर्वसाधारण शेतकऱ्यांना 40% तर SC/ST शेतकऱ्यांना 50% अनुदान मिळते.",
                }
            ],
            "product_review_schema": {
                "name": "बॅटरी स्प्रे पंप 12V 12Ah",
                "rating": 4.6,
                "price_bracket": "₹3,500 - ₹5,200",
                "pros": ["लांब बॅटरी बॅकअप", "डबल मोटर प्रेशर"],
                "cons": ["वजन थोडे जास्त आहे", "लोकल चार्जर वापरू नये"],
            },
        }

        bp = generate_editorial_blueprint(
            seed="बॅटरी स्प्रे पंप",
            language="mr",
            demand=0.78,
            intent="transactional",
            competition_band="low",
            suggestions=["बॅटरी स्प्रे पंप किंमत", "बॅटरी स्प्रे पंप अनुदान"],
            blueprint_type="affiliate",
        )

        self.assertEqual(bp["blueprint_type"], "affiliate")
        self.assertEqual(bp["seed"], "बॅटरी स्प्रे पंप")
        self.assertGreaterEqual(len(bp["paisa_vasool_criteria"]), 2)
        self.assertGreaterEqual(len(bp["verification_checklist"]), 2)
        self.assertIn("बॅटरी स्प्रे पंप", bp["title"])
        self.assertIn("Paisa Vasool Scorecard", bp["markdown_blueprint"])
        self.assertIn("अस्सल की नकली?", bp["markdown_blueprint"])
        self.assertIn("सरकारी अनुदान व योजना", bp["markdown_blueprint"])
        self.assertIn('"@type": "Product"', bp["markdown_blueprint"])
        self.assertIn("Intent Alignment", bp["markdown_blueprint"])
        self.assertIn("Measured Evidence Grounding", bp["markdown_blueprint"])
        self.assertEqual(bp["effective_intent"], "commercial")
        self.assertGreaterEqual(bp["query_coverage_pct"], 50)

    def test_resolve_effective_intent(self):
        """Intent must be dynamically resolved from suggestion evidence when raw intent is unclear."""
        from praman.ai import resolve_effective_intent

        # 1. Commercial suggestions turn unclear raw intent into commercial
        eff_intent, shape = resolve_effective_intent(
            seed="बॅटरी स्प्रे पंप",
            raw_intent="unclear",
            blueprint_type="editorial",
            suggestions=["बॅटरी स्प्रे पंप किंमत", "बॅटरी स्प्रे पंप अनुदान 2026", "बॅटरी स्प्रे पंप वॉरंटी"],
            language="mr",
        )
        self.assertEqual(eff_intent, "commercial")
        self.assertIn("Paisa-Vasool", shape)

        # 2. How-to procedural suggestions turn unclear raw intent into howto
        eff_intent, shape = resolve_effective_intent(
            seed="पीक विमा",
            raw_intent="unclear",
            blueprint_type="editorial",
            suggestions=["पीक विमा कसा काढायचा", "पीक विमा अर्ज पद्धत", "पीक विमा फॉर्म भरणे"],
            language="mr",
        )
        self.assertEqual(eff_intent, "howto")
        self.assertIn("Procedural", shape)

        # 3. Affiliate blueprint type always forces commercial intent
        eff_intent, shape = resolve_effective_intent(
            seed="माहिती",
            raw_intent="informational",
            blueprint_type="affiliate",
            suggestions=[],
            language="mr",
        )
        self.assertEqual(eff_intent, "commercial")


if __name__ == "__main__":
    unittest.main()

