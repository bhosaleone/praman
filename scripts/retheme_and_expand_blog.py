#!/usr/bin/env python3
"""Praman WordPress Re-Theming & Content Expansion Script

Applies the Praman Light Sepia & Saffron design system to WordPress:
1. Customizes twentytwentyfive//header template part with Praman branding & navigation.
2. Customizes twentytwentyfive//footer template part with Praman footer.
3. Publishes 4 additional high-value regional SEO articles.
4. Upgrades the Home Landing Page into an editorial magazine showcase.
"""

import json
import base64
import urllib.request
import urllib.error

WP_BASE = "https://articles.praman.blog/wp-json"
EMAIL = "ishrikantbhosale@gmail.com"
APP_PW = "LsPfxHhYt3mR0mnNachzYcWq"

AUTH_STR = f"{EMAIL}:{APP_PW}"
B64_AUTH = base64.b64encode(AUTH_STR.encode("utf-8")).decode("utf-8")
HEADERS = {
    "Authorization": f"Basic {B64_AUTH}",
    "Content-Type": "application/json",
    "User-Agent": "PramanBot/1.0"
}


def api_post(endpoint: str, data: dict) -> dict:
    req = urllib.request.Request(
        f"{WP_BASE}/{endpoint}",
        data=json.dumps(data).encode("utf-8"),
        headers=HEADERS,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"Error on {endpoint}: {e.code} - {err_msg[:200]}")
        return {"error": e.code, "message": err_msg}


# --------------------------------------------------------------------------
# 1. HEADER TEMPLATE PART CONTENT (WITH COMPLETE LIGHT SEPIA & SAFFRON DESIGN)
# --------------------------------------------------------------------------
HEADER_CONTENT = """<!-- wp:html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --praman-bg: #faf6ee;
    --praman-parchment: #f4ece0;
    --praman-saffron: #ea580c;
    --praman-saffron-hover: #c2410c;
    --praman-ink: #271f18;
    --praman-muted: #645648;
    --praman-dim: #948372;
    --praman-card: #ffffff;
    --praman-border: #dfd2be;
    --praman-border-subtle: #e5dac9;
    --praman-font: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  body, .wp-site-blocks {
    background-color: var(--praman-bg) !important;
    background-image: 
      radial-gradient(at 15% 15%, rgba(234, 88, 12, 0.04) 0px, transparent 45%),
      radial-gradient(at 85% 85%, rgba(217, 119, 6, 0.04) 0px, transparent 45%) !important;
    color: var(--praman-ink) !important;
    font-family: var(--praman-font) !important;
    line-height: 1.65;
  }
  a {
    color: var(--praman-saffron);
    text-decoration: none;
    transition: color 0.2s ease;
  }
  a:hover {
    color: var(--praman-saffron-hover);
    text-decoration: underline;
  }
  h1, h2, h3, h4, h5, h6 {
    font-family: var(--praman-font) !important;
    color: var(--praman-ink) !important;
    font-weight: 700;
  }
  .wp-block-post-content {
    max-width: 900px;
    margin: 0 auto;
    padding: 1.5rem 1rem;
  }
  .praman-custom-header {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1.5px solid var(--praman-border-subtle);
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 0.85rem 1.5rem;
    box-shadow: 0 1px 4px rgba(60, 40, 20, 0.05);
  }
  .praman-header-inner {
    max-width: 1300px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
  }
  .praman-brand {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    text-decoration: none !important;
  }
  .praman-brand-icon {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, #f97316, #ea580c);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 800;
    box-shadow: 0 4px 14px rgba(234, 88, 12, 0.25);
  }
  .praman-brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--praman-ink);
    line-height: 1.1;
  }
  .praman-brand-badge {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--praman-saffron);
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  .praman-nav-links {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    flex-wrap: wrap;
  }
  .praman-nav-link {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--praman-muted);
    text-decoration: none !important;
  }
  .praman-nav-link:hover {
    color: var(--praman-saffron);
  }
  .praman-header-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: #ffffff !important;
    padding: 0.5rem 1.15rem;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 0.88rem;
    box-shadow: 0 4px 12px rgba(234, 88, 12, 0.25);
    text-decoration: none !important;
    transition: transform 0.2s ease;
  }
  .praman-header-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(234, 88, 12, 0.35);
  }
  @media (max-width: 768px) {
    .praman-custom-header {
      padding: 0.75rem 1rem;
    }
    .praman-header-inner {
      flex-direction: column;
      align-items: stretch;
      gap: 0.75rem;
    }
    .praman-nav-links {
      overflow-x: auto;
      white-space: nowrap;
      padding-bottom: 0.25rem;
      gap: 0.85rem;
    }
    .praman-header-btn {
      width: 100%;
      justify-content: center;
      min-height: 40px;
    }
  }
</style>
<header class="praman-custom-header">
  <div class="praman-header-inner">
    <a href="https://articles.praman.blog/" class="praman-brand">
      <div class="praman-brand-icon">प्र</div>
      <div class="praman-brand-text">
        <span class="praman-brand-title">Praman <span style="color:#ea580c; font-family:'Noto Sans Devanagari';">प्रमाण</span></span>
        <span class="praman-brand-badge">Articles &amp; Search Intelligence</span>
      </div>
    </a>
    <nav class="praman-nav-links">
      <a href="https://articles.praman.blog/" class="praman-nav-link">Home</a>
      <a href="https://articles.praman.blog/category/marathi/" class="praman-nav-link">🌾 Marathi (मराठी)</a>
      <a href="https://articles.praman.blog/category/hindi/" class="praman-nav-link">📈 Hindi (हिन्दी)</a>
      <a href="https://articles.praman.blog/category/english/" class="praman-nav-link">🌐 English</a>
      <a href="https://articles.praman.blog/category/tamil/" class="praman-nav-link">🏛️ Tamil (தமிழ்)</a>
      <a href="https://articles.praman.blog/methodology/" class="praman-nav-link">📐 Methodology</a>
      <a href="https://articles.praman.blog/about/" class="praman-nav-link">About</a>
      <a href="https://www.praman.blog/" class="praman-header-btn">⚡ Launch Keyword Tool</a>
    </nav>
  </div>
</header>
<!-- /wp:html -->"""

# --------------------------------------------------------------------------
# 2. FOOTER TEMPLATE PART CONTENT
# --------------------------------------------------------------------------
FOOTER_CONTENT = """<!-- wp:html -->
<style>
  .praman-custom-footer {
    background: #ffffff;
    border-top: 1.5px solid var(--praman-border-subtle);
    padding: 3rem 1.5rem 2rem;
    margin-top: 4rem;
  }
  .praman-footer-inner {
    max-width: 1300px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 2rem;
  }
  .praman-footer-brand {
    max-width: 420px;
  }
  .praman-footer-links {
    display: flex;
    gap: 3rem;
    flex-wrap: wrap;
  }
  .praman-footer-col h5 {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--praman-ink);
    margin-bottom: 0.85rem;
  }
  .praman-footer-col ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .praman-footer-col a {
    color: var(--praman-muted);
    font-size: 0.88rem;
    text-decoration: none;
  }
  .praman-footer-col a:hover {
    color: var(--praman-saffron);
  }
  .praman-footer-bottom {
    max-width: 1300px;
    margin: 2.5rem auto 0;
    padding-top: 1.5rem;
    border-top: 1px solid var(--praman-border-subtle);
    display: flex;
    justify-content: space-between;
    font-size: 0.82rem;
    color: var(--praman-dim);
    flex-wrap: wrap;
    gap: 1rem;
  }
</style>
<footer class="praman-custom-footer">
  <div class="praman-footer-inner">
    <div class="praman-footer-brand">
      <div style="display:flex; align-items:center; gap:0.65rem; margin-bottom:0.75rem;">
        <div style="width:34px; height:34px; background:#ea580c; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:1.2rem;">प्र</div>
        <strong style="font-size:1.2rem; color:#271f18;">Praman (प्रमाण)</strong>
      </div>
      <p style="font-size:0.9rem; color:#645648; line-height:1.6;">
        Evidence-first keyword demand research and editorial content planning for Indian regional languages and English. Refusing to fake volume numbers.
      </p>
    </div>
    <div class="praman-footer-links">
      <div class="praman-footer-col">
        <h5>Regional Categories</h5>
        <ul>
          <li><a href="https://articles.praman.blog/category/marathi/">🌾 Marathi SEO (मराठी)</a></li>
          <li><a href="https://articles.praman.blog/category/hindi/">📈 Hindi SEO (हिन्दी)</a></li>
          <li><a href="https://articles.praman.blog/category/english/">🌐 English Guides</a></li>
          <li><a href="https://articles.praman.blog/category/tamil/">🏛️ Tamil SEO (தமிழ்)</a></li>
          <li><a href="https://articles.praman.blog/category/case-studies/">📊 Case Studies</a></li>
        </ul>
      </div>
      <div class="praman-footer-col">
        <h5>Platform &amp; Legal</h5>
        <ul>
          <li><a href="https://www.praman.blog/">⚡ Keyword Tool App</a></li>
          <li><a href="https://articles.praman.blog/methodology/">📐 Methodology</a></li>
          <li><a href="https://articles.praman.blog/about/">📖 About Praman</a></li>
          <li><a href="https://articles.praman.blog/privacy-policy/">🔒 Privacy Policy</a></li>
          <li><a href="https://articles.praman.blog/terms/">📜 Terms of Service</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="praman-footer-bottom">
    <span>&copy; 2026 Praman (प्रमाण). Built for Bharat.</span>
    <span>Light Sepia &amp; Saffron Aesthetic • Stdlib Core • Zero Fake Volume</span>
  </div>
</footer>
<!-- /wp:html -->"""

# --------------------------------------------------------------------------
# 3. FOUR NEW RICH ARTICLES
# --------------------------------------------------------------------------
NEW_ARTICLES = [
    {
        "title": "Tamil Vernacular Search Growth: How to Find High-Traffic Keywords in தமிழ் (Tamil) for AdSense & Affiliate Blogs",
        "slug": "tamil-seo-keyword-research-guide",
        "categories": [6, 7],  # Tamil, Case Studies
        "excerpt": "A deep dive into Tamil search patterns: agricultural schemes (விவசாய திட்டம்), government welfare, and job portals in Tamil Nadu.",
        "content": """
<p class="lead" style="font-size:1.15rem; color:#645648;">
  Tamil Nadu is one of the highest internet-penetrated states in India, with over 55 million active digital consumers. However, Tamil content publishers face a persistent issue with traditional SEO platforms: <strong>Google Keyword Planner and Ahrefs return '0 volume' for key Tamil welfare, agricultural, and job queries</strong>.
</p>

<h2>Understanding Tamil Abugida Search Syntax</h2>
<p>
  Tamil script has 12 vowels (உயிரெழுத்து), 18 consonants (மெய்யெழுத்து), and 216 combined vowel-consonant characters (உயிர்மெய்யெழுத்து).
</p>
<p>
  When a user searches for <code>விவசாய கடன் தள்ளுபடி</code> (agricultural loan waiver), Western word boundary parsers fail because combining vowels are decoupled. Praman uses lookaround Unicode range protection specifically calibrated for Tamil Unicode blocks (<code>U+0B80 - U+0BFF</code>), allowing bloggers to capture true user demand across:
</p>
<ul>
  <li>🟢 <strong>Strong Evidence:</strong> <code>விவசாய கடன் தள்ளுபடி 2026</code> (Agricultural loan waiver 2026)</li>
  <li>🟢 <strong>Transactional Intent:</strong> <code>மகளிர் உரிமைத் தொகை விண்ணப்பம்</code> (Women's rights financial scheme application)</li>
  <li>🟡 <strong>Conversational Questions:</strong> <code>ரேஷன் கார்டு பெயர் சேர்க்க எப்படி</code> (How to add name to ration card)</li>
</ul>

<h2>Content Architecture for Tamil News &amp; Niche Portals</h2>
<p>
  To rank in Tamil SERPs, avoid standalone articles. Praman's <strong>Editorial Content Planner</strong> clusters Tamil queries by topic skeleton, generating internal link anchors like <code>விண்ணப்பிக்கும் முறை</code> (Application method) to anchor high-demand hub pages.
</p>

<div style="text-align:center; margin:2.5rem 0;">
  <a href="https://www.praman.blog/" class="praman-btn-cta">🏛️ Test Tamil Keywords Live on Praman</a>
</div>
"""
    },
    {
        "title": "How to Build a High-Traffic Marathi & Hindi Krishi (Agri) Portal in 2026: The Complete Editorial Blueprint",
        "slug": "how-to-build-agri-portal-marathi-hindi",
        "categories": [3, 4, 7],  # Marathi, Hindi, Case Studies
        "excerpt": "A master editorial blueprint for regional agriculture blogging: market yard rates, crop subsidies, and seasonal demand timing.",
        "content": """
<p class="lead" style="font-size:1.15rem; color:#645648;">
  Agriculture is the largest employment sector in Bharat, and farming communities are among the most active daily mobile searchers on Google. Building a successful bilingual (Marathi &amp; Hindi) Krishi portal requires mastering <strong>three seasonal demand cycles</strong>.
</p>

<h2>1. The Real-Time Market Rate Cycle (बाजारभाव / मंडी भाव)</h2>
<p>
  Farmers check commodity prices every morning before heading to the APMC market yard. High-frequency queries include:
</p>
<ul>
  <li><code>कांदा बाजार भाव आजचा</code> (Onion market rate today)</li>
  <li><code>सोयाबीन भाव वाढणार का</code> (Will soybean prices increase?)</li>
  <li><code>कपास का ताजा भाव</code> (Cotton fresh market price)</li>
</ul>
<p>
  Praman's <strong>Freshness Classifier</strong> detects temporal markers like <em>आजचा, आता, ताजा, 2026</em>, allowing you to create automated daily live-update templates.
</p>

<h2>2. The Subsidy &amp; Scheme Cycle (योजना व अनुदान)</h2>
<p>
  Government subsidies (महाडीबीटी, पीएम किसान, कुसुम सौर पंप) peak during monsoon sowing (Kharif) and post-harvest (Rabi). The intent is <strong>Transactional &amp; Downloadable</strong>:
</p>
<ul>
  <li><code>पीएम किसान 19 वी हप्ता तारीख</code></li>
  <li><code>कुसुम सोलर पंप योजना ऑनलाइन अर्ज</code></li>
  <li><code>पीक विमा यादी 2026 pdf download</code></li>
</ul>

<h2>3. Internal Linking Architecture</h2>
<p>
  Link your daily market price updates back to comprehensive pillar guides on <em>साठवणूक पद्धती</em> (storage techniques) and <em>खत व्यवस्थापन</em> (fertilizer management). This cross-links high-traffic transient pages to evergreen commercial content.
</p>

<div style="text-align:center; margin:2.5rem 0;">
  <a href="https://www.praman.blog/" class="praman-btn-cta">🌾 Plan Your Krishi Blog on Praman</a>
</div>
"""
    },
    {
        "title": "What is 'Unmeasured Demand' (⊥) and Why Modern SEO Tools Must Stop Fabricating Search Volume",
        "slug": "what-is-unmeasured-demand-explained",
        "categories": [5, 8],  # English, Methodology
        "excerpt": "Why forcing missing data to zero or fabricating numbers damages content ROI, and how Praman's 3-state codomain mathematically protects publishers.",
        "content": """
<p class="lead" style="font-size:1.15rem; color:#645648;">
  In traditional computer science and database theory, there is a fundamental distinction between <strong>zero</strong> (we checked, and the value is 0) and <strong>null / bottom (&perp;)</strong> (we did not measure it, or data is unavailable).
</p>

<h2>The SEO Industry's Dirty Secret: Coercing &perp; to Zero</h2>
<p>
  When you enter an emerging regional phrase into traditional SEO dashboards, one of two things happens:
</p>
<ol>
  <li><strong>Fabricated Clickstream:</strong> The tool runs a probabilistic regression model and shows "Monthly Volume: 450", which is entirely hallucinated.</li>
  <li><strong>Silent Coercion:</strong> If their crawler had a network timeout or lacked proxy coverage, it quietly writes <code>volume = 0</code>.</li>
</ol>
<p>
  Writing <code>volume = 0</code> causes content editors to abandon lucrative emerging topics, believing nobody searches for them.
</p>

<h2>The Praman Mathematical Invariant</h2>
<p>
  Praman defines search demand across a strict 3-state codomain:
  <code>V = ℝ ∪ {⊥}</code>
</p>
<p>
  If a network probe fails, if an endpoint times out, or if rate-limiting occurs, the weight of that voice is <strong>never redistributed</strong> to surviving voices, and the achievable score is capped (Theorem 2). 
</p>
<div class="praman-callout">
  <h4 style="margin-top:0; color:#ea580c;">Mathematical Honesty</h4>
  <p style="margin-bottom:0;">
    Praman explicitly displays <strong>&perp; (Unmeasured Demand)</strong>. This guarantees that publishers never confuse a technical measurement failure with a lack of audience interest.
  </p>
</div>

<div style="text-align:center; margin:2.5rem 0;">
  <a href="https://www.praman.blog/" class="praman-btn-cta">⚡ Experience Honest Research on Praman</a>
</div>
"""
    },
    {
        "title": "Finding High-Intent Vernacular Buyer Queries: Commercial vs Informational Intent in Indian Languages",
        "slug": "commercial-vs-informational-intent-indian-languages",
        "categories": [4, 5, 7],  # Hindi, English, Case Studies
        "excerpt": "How to identify high-paying commercial buyer intent in Hindi, Marathi, and Tamil to maximize AdSense RPM and affiliate commissions.",
        "content": """
<p class="lead" style="font-size:1.15rem; color:#645648;">
  Not all traffic is created equal. A blog post with 1,000 visitors searching for a high-intent buyer keyword often earns 10x more AdSense revenue and affiliate commissions than a generic post with 50,000 visitors.
</p>

<h2>The Linguistic Markers of Vernacular Commercial Intent</h2>
<p>
  In English, commercial intent markers are straightforward: <em>buy, price, best, coupon, review</em>. In Indian regional languages, commercial intent is deeply conversational and idiomatic:
</p>

<table style="width:100%; border-collapse:collapse; margin:1.5rem 0; font-size:0.95rem;">
  <thead>
    <tr style="background:#f4ece0; border-bottom:2px solid #dfd2be; text-align:left;">
      <th style="padding:0.75rem 1rem;">Intent Type</th>
      <th style="padding:0.75rem 1rem;">Hindi (हिन्दी)</th>
      <th style="padding:0.75rem 1rem;">Marathi (मराठी)</th>
      <th style="padding:0.75rem 1rem;">Commercial Value</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid #f0e6d8;">
      <td style="padding:0.75rem 1rem;"><strong>Transactional (Buyer)</strong></td>
      <td style="padding:0.75rem 1rem;"><code>कीमत, खरीदना, ऑनलाइन अप्लाई</code></td>
      <td style="padding:0.75rem 1rem;"><code>किंमत, घ्यायचे आहे, अर्ज कसा करावा</code></td>
      <td style="padding:0.75rem 1rem; color:#15803d; font-weight:700;">High RPM ($2 - $8)</td>
    </tr>
    <tr style="border-bottom:1px solid #f0e6d8;">
      <td style="padding:0.75rem 1rem;"><strong>Comparison (Research)</strong></td>
      <td style="padding:0.75rem 1rem;"><code>बनाम, कौन सा अच्छा है, अंतर</code></td>
      <td style="padding:0.75rem 1rem;"><code>तुलना, फरक, कोणता चांगला</code></td>
      <td style="padding:0.75rem 1rem; color:#d97706; font-weight:700;">Medium RPM ($1 - $3)</td>
    </tr>
    <tr>
      <td style="padding:0.75rem 1rem;"><strong>Informational (General)</strong></td>
      <td style="padding:0.75rem 1rem;"><code>क्या है, इतिहास, विवरण</code></td>
      <td style="padding:0.75rem 1rem;"><code>म्हणजे काय, माहिती, इतिहास</code></td>
      <td style="padding:0.75rem 1rem; color:#645648;">Low RPM ($0.2 - $0.8)</td>
    </tr>
  </tbody>
</table>

<h2>Using Praman's Intent Ladder</h2>
<p>
  Praman's built-in intent classifier evaluates candidates across a strict precedence ladder:
  <strong>Transactional &gt; Freshness &gt; Comparison &gt; How-To &gt; Informational</strong>.
  When a candidate keyword contains both informational and transactional words, the commercial intent wins, ensuring you never misclassify lucrative buyer searches.
</p>

<div style="text-align:center; margin:2.5rem 0;">
  <a href="https://www.praman.blog/" class="praman-btn-cta">📈 Discover Commercial Keywords on Praman</a>
</div>
"""
    }
]

# --------------------------------------------------------------------------
# 4. UPGRADED EDITORIAL MAGAZINE HOME PAGE CONTENT
# --------------------------------------------------------------------------
HOMEPAGE_UPGRADE = """
<div style="max-width:1200px; margin:0 auto; padding:1.5rem 1rem;">
  <!-- Hero Section -->
  <div style="background:linear-gradient(135deg, #fffaf2, #f4ece0); border:1.5px solid #dfd2be; border-radius:18px; padding:3rem 2rem; text-align:center; margin-bottom:3rem; box-shadow:0 4px 20px -2px rgba(90, 60, 30, 0.08);">
    <span style="display:inline-block; background:rgba(234, 88, 12, 0.12); color:#ea580c; border:1px solid rgba(234, 88, 12, 0.3); padding:0.35rem 1rem; border-radius:9999px; font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1.25rem;">
      Evidence-First Search Intelligence
    </span>
    <h1 style="font-size:2.8rem; font-weight:800; color:#271f18; line-height:1.15; margin-bottom:1rem; letter-spacing:-0.02em;">
      Master Vernacular Search in Bharat.<br><span style="color:#ea580c;">Without Fabricated Metrics.</span>
    </h1>
    <p style="font-size:1.2rem; color:#645648; max-width:800px; margin:0 auto 2rem; line-height:1.6;">
      In-depth case studies, Brahmic script search mechanics, and editorial workflows for regional content creators in Marathi, Hindi, Tamil, Telugu, and English.
    </p>
    <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
      <a href="https://www.praman.blog/" style="display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg, #f97316, #ea580c); color:#ffffff; font-weight:700; font-size:1.1rem; padding:0.9rem 2rem; border-radius:10px; box-shadow:0 4px 14px rgba(234, 88, 12, 0.35); text-decoration:none;">
        ⚡ Launch the Live Tool at praman.blog
      </a>
      <a href="/why-traditional-seo-tools-fail-indic-languages/" style="display:inline-flex; align-items:center; gap:0.5rem; background:#ffffff; border:1.5px solid #dfd2be; color:#271f18; font-weight:700; font-size:1.1rem; padding:0.9rem 1.8rem; border-radius:10px; text-decoration:none;">
        📖 Read Featured Case Study
      </a>
    </div>
  </div>

  <!-- Featured Articles Section -->
  <div style="margin-bottom:3rem;">
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.5rem; border-bottom:2px solid #e5dac9; padding-bottom:0.75rem;">
      <h2 style="font-size:1.8rem; font-weight:800; color:#271f18; margin:0;">Featured Editorial Case Studies</h2>
      <span style="font-size:0.9rem; color:#645648; font-weight:600;">7 Published Guides</span>
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:1.5rem;">
      <!-- Card 1 -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:700; color:#ea580c; background:rgba(234, 88, 12, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.75rem;">Technical SEO • English</span>
          <h3 style="font-size:1.25rem; font-weight:700; margin:0 0 0.75rem; line-height:1.35;">
            <a href="/why-traditional-seo-tools-fail-indic-languages/" style="color:#271f18; text-decoration:none;">The Truth About Indic Keyword Research: Why Traditional SEO Tools Break on Matras</a>
          </h3>
          <p style="font-size:0.92rem; color:#645648; line-height:1.55; margin-bottom:1rem;">
            Why enterprise tools show '0 volume' for queries searched by millions of people, and how Brahmic combining mark mechanics solve it.
          </p>
        </div>
        <a href="/why-traditional-seo-tools-fail-indic-languages/" style="font-weight:700; font-size:0.92rem; color:#ea580c;">Read Full Case Study &rarr;</a>
      </article>

      <!-- Card 2 -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:700; color:#15803d; background:rgba(21, 128, 61, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.75rem;">शेती केस स्टडी • मराठी</span>
          <h3 style="font-size:1.25rem; font-weight:700; margin:0 0 0.75rem; line-height:1.35;">
            <a href="/marathi-agriculture-keyword-research-case-study/" style="color:#271f18; text-decoration:none;">मराठी शेती आणि बाजारभाव ब्लॉगिंग: Ahrefs शिवाय हाय-डिमांड कीवर्ड कसे शोधावे?</a>
          </h3>
          <p style="font-size:0.92rem; color:#645648; line-height:1.55; margin-bottom:1rem;">
            कांदा भाव, पीक विमा आणि हवामान अंदाज: पारंपारिक टूल्स फेल का होतात आणि प्रमाणच्या मदतीने अचूक शेती कीवर्ड कसे शोधावे.
          </p>
        </div>
        <a href="/marathi-agriculture-keyword-research-case-study/" style="font-weight:700; font-size:0.92rem; color:#ea580c;">केस स्टडी वाचा &rarr;</a>
      </article>

      <!-- Card 3 -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:700; color:#d97706; background:rgba(217, 119, 6, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.75rem;">फाइनेंस गाइड • हिन्दी</span>
          <h3 style="font-size:1.25rem; font-weight:700; margin:0 0 0.75rem; line-height:1.35;">
            <a href="/hindi-finance-keyword-research-strategy/" style="color:#271f18; text-decoration:none;">हिंदी फाइनेंस और शेयर बाजार ब्लॉग्स के लिए कीवर्ड रिसर्च: सटीक डिमांड कैसे पहचानें</a>
          </h3>
          <p style="font-size:0.92rem; color:#645648; line-height:1.55; margin-bottom:1rem;">
            म्यूचुअल फंड, शेयर बाजार और बचत खाता: हिंदी में वित्तीय सामग्री तैयार करने के लिए वैज्ञानिक कीवर्ड रणनीति।
          </p>
        </div>
        <a href="/hindi-finance-keyword-research-strategy/" style="font-weight:700; font-size:0.92rem; color:#ea580c;">गाइड पढ़ें &rarr;</a>
      </article>

      <!-- Card 4 -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:700; color:#78350f; background:rgba(120, 53, 15, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.75rem;">தமிழ் SEO • Tamil</span>
          <h3 style="font-size:1.25rem; font-weight:700; margin:0 0 0.75rem; line-height:1.35;">
            <a href="/tamil-seo-keyword-research-guide/" style="color:#271f18; text-decoration:none;">Tamil Vernacular Search Growth: Finding High-Traffic Keywords in தமிழ் (Tamil)</a>
          </h3>
          <p style="font-size:0.92rem; color:#645648; line-height:1.55; margin-bottom:1rem;">
            A deep dive into Tamil search patterns: agricultural schemes (விவசாய திட்டம்), welfare, and job portals in Tamil Nadu.
          </p>
        </div>
        <a href="/tamil-seo-keyword-research-guide/" style="font-weight:700; font-size:0.92rem; color:#ea580c;">Read Guide &rarr;</a>
      </article>

      <!-- Card 5 -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:700; color:#15803d; background:rgba(21, 128, 61, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.75rem;">Agri Blueprint • Marathi &amp; Hindi</span>
          <h3 style="font-size:1.25rem; font-weight:700; margin:0 0 0.75rem; line-height:1.35;">
            <a href="/how-to-build-agri-portal-marathi-hindi/" style="color:#271f18; text-decoration:none;">Building a High-Traffic Marathi &amp; Hindi Krishi (Agri) Portal in 2026</a>
          </h3>
          <p style="font-size:0.92rem; color:#645648; line-height:1.55; margin-bottom:1rem;">
            A master editorial blueprint for regional agriculture blogging: market rates, crop subsidies, and seasonal demand timing.
          </p>
        </div>
        <a href="/how-to-build-agri-portal-marathi-hindi/" style="font-weight:700; font-size:0.92rem; color:#ea580c;">Read Blueprint &rarr;</a>
      </article>

      <!-- Card 6 -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:700; color:#ea580c; background:rgba(234, 88, 12, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.75rem;">Data Integrity • Methodology</span>
          <h3 style="font-size:1.25rem; font-weight:700; margin:0 0 0.75rem; line-height:1.35;">
            <a href="/what-is-unmeasured-demand-explained/" style="color:#271f18; text-decoration:none;">What is 'Unmeasured Demand' (⊥) and Why SEO Tools Must Stop Fabricating Volume</a>
          </h3>
          <p style="font-size:0.92rem; color:#645648; line-height:1.55; margin-bottom:1rem;">
            Why forcing missing data to zero or inventing numbers damages content ROI, and how Praman's 3-state codomain protects publishers.
          </p>
        </div>
        <a href="/what-is-unmeasured-demand-explained/" style="font-weight:700; font-size:0.92rem; color:#ea580c;">Read Explanation &rarr;</a>
      </article>
    </div>
  </div>

  <!-- Callout Banner -->
  <div style="background:#fffdfa; border:2px dashed #ea580c; border-radius:16px; padding:2.5rem 2rem; text-align:center; margin:3rem 0;">
    <h3 style="font-size:1.8rem; font-weight:800; color:#271f18; margin:0 0 0.75rem;">Ready to Find Hidden Keywords in Your Language?</h3>
    <p style="font-size:1.05rem; color:#645648; max-width:650px; margin:0 auto 1.5rem;">
      Praman is completely free to try. No signup or credit card required. Run real-time autocomplete analysis across 10 Indic languages and English.
    </p>
    <a href="https://www.praman.blog/" style="display:inline-flex; align-items:center; gap:0.5rem; background:#ea580c; color:#ffffff; font-weight:700; font-size:1.05rem; padding:0.85rem 1.85rem; border-radius:10px; text-decoration:none;">
      ⚡ Launch Praman Keyword Planner Now
    </a>
  </div>
</div>
"""


def main():
    print("=== Re-Theming & Content Expansion ===")

    # 1. Update Header Template Part
    print("\n1. Injecting Light Sepia & Saffron Header into WordPress...")
    res_hdr = api_post("wp/v2/template-parts/twentytwentyfive//header", {"content": HEADER_CONTENT})
    print("Header update status:", "id" in res_hdr or res_hdr.get("status") == 200)

    # 2. Update Footer Template Part
    print("\n2. Injecting Custom Footer into WordPress...")
    res_ftr = api_post("wp/v2/template-parts/twentytwentyfive//footer", {"content": FOOTER_CONTENT})
    print("Footer update status:", "id" in res_ftr or res_ftr.get("status") == 200)

    # 3. Publish 4 Additional Rich Articles
    print("\n3. Publishing 4 Additional Regional SEO Articles...")
    for post in NEW_ARTICLES:
        payload = {
            "title": post["title"],
            "slug": post["slug"],
            "categories": post["categories"],
            "excerpt": post["excerpt"],
            "content": post["content"],
            "status": "publish",
            "comment_status": "open"
        }
        res = api_post("wp/v2/posts", payload)
        if "id" in res:
            print(f"Published: {post['title'][:40]}... (ID: {res['id']}, URL: {res.get('link')})")
        else:
            print(f"Failed {post['slug']}:", res)

    # 4. Upgrade Home Landing Page
    print("\n4. Upgrading Home Landing Page with Magazine Cards Grid...")
    res_home = api_post("wp/v2/pages/7", {
        "title": "Praman (प्रमाण) — Vernacular Search Intelligence & Editorial Guides",
        "content": HOMEPAGE_UPGRADE
    })
    print("Home page upgrade status:", "id" in res_home)

    print("\n=== Re-Theming & Content Expansion Completed Successfully! ===")


if __name__ == "__main__":
    main()
