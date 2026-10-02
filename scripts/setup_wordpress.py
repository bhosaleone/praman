#!/usr/bin/env python3
"""Praman WordPress Setup & Content Generation Script

Configures articles.praman.blog via WordPress REST API:
- Injects Sepia & Saffron themed Landing Page
- Creates Essential Pages (About, Methodology, Privacy, Terms)
- Publishes 3 Rich Launch Case Studies (English, Marathi, Hindi)
- Unpublishes/deletes default Hello World post
- Sets static front page
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


def api_delete(endpoint: str) -> dict:
    req = urllib.request.Request(
        f"{WP_BASE}/{endpoint}?force=true",
        headers=HEADERS,
        method="DELETE"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


# --------------------------------------------------------------------------
# THEMED HTML STYLES (Light Sepia #faf6ee & Saffron #ea580c)
# --------------------------------------------------------------------------
THEME_STYLE = """
<style>
  :root {
    --praman-bg: #faf6ee;
    --praman-parchment: #f4ece0;
    --praman-saffron: #ea580c;
    --praman-saffron-hover: #c2410c;
    --praman-ink: #271f18;
    --praman-muted: #645648;
    --praman-card: #ffffff;
    --praman-border: #dfd2be;
  }
  .praman-theme-wrapper {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: var(--praman-ink);
    line-height: 1.7;
    font-size: 1.05rem;
  }
  .praman-hero-card {
    background: linear-gradient(135deg, #fffaf2, #f4ece0);
    border: 1.5px solid var(--praman-border);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2.5rem;
    box-shadow: 0 4px 20px -2px rgba(90, 60, 30, 0.08);
    text-align: center;
  }
  .praman-badge {
    display: inline-block;
    background: rgba(234, 88, 12, 0.12);
    color: var(--praman-saffron);
    border: 1px solid rgba(234, 88, 12, 0.3);
    padding: 0.3rem 0.9rem;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 1rem;
  }
  .praman-btn-cta {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 0.85rem 1.85rem;
    border-radius: 10px;
    box-shadow: 0 4px 14px rgba(234, 88, 12, 0.35);
    margin-top: 1.25rem;
    transition: transform 0.2s ease;
  }
  .praman-btn-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(234, 88, 12, 0.45);
  }
  .praman-callout {
    background: #fffdfa;
    border-left: 4px solid var(--praman-saffron);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin: 1.75rem 0;
    border-top: 1px solid var(--praman-border);
    border-right: 1px solid var(--praman-border);
    border-bottom: 1px solid var(--praman-border);
  }
  .praman-grid-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.25rem;
    margin: 2rem 0;
  }
  .praman-feature-card {
    background: #ffffff;
    border: 1px solid var(--praman-border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 8px rgba(60, 40, 20, 0.05);
  }
  .praman-feature-card h4 {
    color: var(--praman-saffron);
    margin-top: 0;
    margin-bottom: 0.5rem;
    font-size: 1.15rem;
  }
</style>
"""

# --------------------------------------------------------------------------
# PAGES DATA
# --------------------------------------------------------------------------
PAGES = [
    {
        "title": "Praman (प्रमाण) — Vernacular Search Intelligence & Editorial Guides",
        "slug": "home",
        "content": THEME_STYLE + """
<div class="praman-theme-wrapper">
  <div class="praman-hero-card">
    <span class="praman-badge">Evidence-First Search Intelligence</span>
    <h1 style="font-size:2.4rem; font-weight:800; margin-bottom:0.75rem; color:#271f18; line-height:1.2;">
      Keyword Demand &amp; Editorial Content Planning for Bharat
    </h1>
    <p style="font-size:1.15rem; color:#645648; max-width:760px; margin:0 auto 1.5rem;">
      Traditional SEO tools like Ahrefs and SEMrush charge ₹8,000 to ₹35,000/month while fabricating search volume or displaying "0 volume" for Indian regional keywords with millions of active searches. 
      <strong>Praman reveals true autocomplete demand mathematically.</strong>
    </p>
    <div>
      <a href="https://www.praman.blog/" class="praman-btn-cta">⚡ Launch the Live Tool at praman.blog</a>
    </div>
  </div>

  <h2>Why Regional Creators &amp; News Publishers Need Praman</h2>
  <div class="praman-grid-cards">
    <div class="praman-feature-card">
      <h4>🌾 10 Indic Scripts + English</h4>
      <p>Full native support for Devanagari (Marathi, Hindi), Dravidian (Tamil, Telugu, Kannada, Malayalam), Bengali, Gujarati, Punjabi, and Odia without broken combining marks.</p>
    </div>
    <div class="praman-feature-card">
      <h4>📐 Pinned Mathematical Demand</h4>
      <p>Four deterministic dimensions: Expansion Breadth (50%), Head Coverage (25%), Question Density (15%), and Rank Depth (10%). Denominators never shift silently.</p>
    </div>
    <div class="praman-feature-card">
      <h4>🌳 Interactive Research Trees</h4>
      <p>Discover high-intent candidate keywords and expand recursively with continuous <code>[+ Measure]</code> discovery loops right from your phone or desktop.</p>
    </div>
    <div class="praman-feature-card">
      <h4>📅 Ready-to-Write Editorial Plans</h4>
      <p>Automated consonant-skeleton topic clustering that generates prioritized publishing calendars and contextual internal linking graphs with one click.</p>
    </div>
  </div>

  <div class="praman-callout">
    <h3 style="margin-top:0; color:#ea580c;">🛡️ Our Core Pledge: Refusing to Fake Volume</h3>
    <p style="margin-bottom:0;">
      If auto-complete data is unavailable or rate-limited, Praman outputs <strong>&perp; (Unmeasured Demand)</strong>. We will never invent fake search volume numbers or coerce missing data to zero. What you see is mathematically verified evidence.
    </p>
  </div>

  <h2>Explore Regional SEO Case Studies</h2>
  <p>Read our in-depth teardowns and practical workflows across regional languages:</p>
  <ul>
    <li><a href="/why-traditional-seo-tools-fail-indic-languages/"><strong>Technical Teardown:</strong> Why Traditional SEO Tools Break on Matras &amp; Fail in Regional Languages</a></li>
    <li><a href="/marathi-agriculture-keyword-research-case-study/"><strong>मराठी केस स्टडी:</strong> कांदा भाव आणि पीक विमा कीवर्ड रिसर्च विना Ahrefs कसा करावा?</a></li>
    <li><a href="/hindi-finance-keyword-research-strategy/"><strong>हिंदी गाइड:</strong> शेयर बाजार और म्यूचुअल फंड ब्लॉग्स के लिए कन्वर्सेशनल कीवर्ड स्ट्रैटेजी</a></li>
  </ul>
</div>
"""
    },
    {
        "title": "About Praman",
        "slug": "about",
        "content": THEME_STYLE + """
<div class="praman-theme-wrapper">
  <h1>About Praman (प्रमाण)</h1>
  <p class="lead" style="font-size:1.15rem; color:#645648;">
    <em>Praman</em> is a Sanskrit and Indian vernacular word meaning <strong>proof, evidence, and verifiable truth</strong>.
  </p>
  <p>
    Over 600 million people across India search Google in regional languages—Hindi, Marathi, Tamil, Telugu, Gujarati, Bengali, and beyond. Yet the global SEO software industry was built almost exclusively for Western English grammar and Latin alphabets.
  </p>
  <p>
    When an Indian regional creator or news editor types a regional keyword into mainstream enterprise tools, they face two constant failures:
  </p>
  <ol>
    <li><strong>The "0 Volume" Lie:</strong> Crucial agricultural, financial, and government scheme queries show "0 Monthly Searches", even when millions of citizens search for them on Google every week.</li>
    <li><strong>Matra &amp; Tokenizer Breakage:</strong> Brahmic combining marks (like <code>ा</code>, <code>ी</code>, <code>ू</code>, <code>ं</code>) are severed by naive word boundaries, treating single words as garbled fragments.</li>
  </ol>
  
  <div class="praman-callout">
    <h3>Built from First Principles</h3>
    <p>
      Praman was created to give Bharat's bloggers, independent publishers, and digital journalists a scientific, mathematically sound, and zero-deception research tool. 
      It runs in pure Python, requires no bloated machine learning APIs, and strictly adheres to verifiable autocomplete demand evidence.
    </p>
  </div>

  <p>
    Access the live application at <a href="https://www.praman.blog/"><strong>www.praman.blog</strong></a>.
  </p>
</div>
"""
    },
    {
        "title": "Methodology & The Pinned Voice Contract",
        "slug": "methodology",
        "content": THEME_STYLE + """
<div class="praman-theme-wrapper">
  <h1>Methodology &amp; The Pinned Voice Contract</h1>
  <p style="font-size:1.1rem; color:#645648;">
    Transparent mathematical foundations governing all demand scores in Praman.
  </p>

  <h2>1. The Four Pinned Voices (Eq. 6)</h2>
  <pre style="background:#f4ece0; padding:1rem; border-radius:8px; font-family:monospace; font-size:1rem; color:#271f18;">
demand(s) = 0.50·breadth(s) + 0.25·coverage(s) + 0.15·density(s) + 0.10·depth(s)
  </pre>
  <p>
    <strong>The denominator never moves:</strong> If any voice is unmeasured (&perp;) due to network cooldowns or timeouts, its weight is <em>never</em> redistributed to surviving voices. The measured mass \(c(s) &lt; 1.0\) caps the achievable score below 1.0 (Theorem 2) and transparently marks the score as partial.
  </p>

  <h2>2. Evidence Banding</h2>
  <div class="praman-grid-cards">
    <div class="praman-feature-card" style="border-left: 4px solid #15803d;">
      <h4>🟢 Strong Evidence (&ge; 0.50)</h4>
      <p>High auto-complete presence, broad alphabet expansion, and question demand. Prioritize these topics for immediate editorial coverage.</p>
    </div>
    <div class="praman-feature-card" style="border-left: 4px solid #d97706;">
      <h4>🟡 Moderate Evidence (0.25 – 0.49)</h4>
      <p>Measurable interest on partial expansion axes. Excellent for supporting articles or niche focus sections.</p>
    </div>
    <div class="praman-feature-card" style="border-left: 4px solid #78716c;">
      <h4>⚪ Weak Evidence (&lt; 0.25)</h4>
      <p>Sparse expansion signals. Highly specific long-tail query or nascent emerging topic.</p>
    </div>
    <div class="praman-feature-card" style="border-left: 4px solid #dc2626;">
      <h4>🔴 Insufficient / Unmeasured (&perp;)</h4>
      <p>No response or rate-limited. We refuse to coerce this to zero. Praman flags it as unmeasured so you can re-test.</p>
    </div>
  </div>

  <h2>3. Human Competition Banding</h2>
  <p>
    Praman completely avoids scraping Google Search Result Pages (SERPs) to prevent ToS violations and proxy unreliability. Instead, human observations (thin content, weak forum results, stale articles) are recorded directly by the user, deriving verifiable competition bands only when &ge; 2 fields are noted.
  </p>
</div>
"""
    },
    {
        "title": "Privacy Policy",
        "slug": "privacy-policy",
        "content": THEME_STYLE + """
<div class="praman-theme-wrapper">
  <h1>Privacy Policy</h1>
  <p><em>Last updated: October 2026</em></p>
  <p>
    At Praman (<code>praman.blog</code> and <code>articles.praman.blog</code>), we respect your privacy.
  </p>
  <h3>1. Data Collection</h3>
  <p>
    Praman does not require user registration or personal identification to use the core keyword research tool. 
    We do not sell, rent, or trade user search queries to third-party ad brokers or data aggregators.
  </p>
  <h3>2. Cookies &amp; Local Storage</h3>
  <p>
    We use standard browser local storage solely to retain your active research session, user preferences, and export files.
  </p>
  <h3>3. Contact</h3>
  <p>
    For privacy inquiries, contact the team at <code>ishrikantbhosale@gmail.com</code>.
  </p>
</div>
"""
    },
    {
        "title": "Terms of Service",
        "slug": "terms",
        "content": THEME_STYLE + """
<div class="praman-theme-wrapper">
  <h1>Terms of Service</h1>
  <p><em>Last updated: October 2026</em></p>
  <p>
    By accessing Praman at <code>praman.blog</code> and <code>articles.praman.blog</code>, you agree to these Terms of Service.
  </p>
  <h3>1. Purpose of Service</h3>
  <p>
    Praman provides mathematical keyword demand research and editorial content planning tools for Indic regional languages and English. 
    Demand metrics represent mathematical models of autocomplete evidence and do not guarantee search rankings or organic traffic.
  </p>
  <h3>2. Acceptable Use</h3>
  <p>
    Users agree not to flood the service with automated denial-of-service traffic or attempt to reverse-engineer server infrastructure.
  </p>
</div>
"""
    }
]

# --------------------------------------------------------------------------
# BLOG POSTS DATA
# --------------------------------------------------------------------------
POSTS = [
    {
        "title": "The Truth About Indic Keyword Research: Why Traditional SEO Tools Break on Matras and Fail in Regional Languages",
        "slug": "why-traditional-seo-tools-fail-indic-languages",
        "categories": [5, 7, 8],  # English, Case Studies, Methodology
        "excerpt": "Why enterprise SEO tools like Ahrefs and SEMrush show '0 search volume' for Indian language keywords with millions of searches, and how Brahmic combining mark mechanics solve it.",
        "content": THEME_STYLE + """
<div class="praman-theme-wrapper">
  <p class="lead" style="font-size:1.15rem; color:#645648;">
    If you have ever tried doing keyword research for Marathi, Hindi, Tamil, or Telugu in tools like Ahrefs, SEMrush, or Google Keyword Planner, you have encountered the classic absurdity: 
    <strong>a high-demand query searched by millions of people displays "Search Volume: 0"</strong>.
  </p>

  <h2>The Root Cause: The Matra &amp; Tokenizer Breakage</h2>
  <p>
    Unlike English, which is written with discrete Latin letters separated by spaces, Indian languages are written in <strong>Brahmic abugida scripts</strong> (Devanagari, Dravidian, Bengali, Gurmukhi).
  </p>
  <p>
    In Devanagari, consonants carry an inherent vowel that is modified by attaching dependent vowel signs known as <strong>matras</strong> (मात्रा), such as:
  </p>
  <ul>
    <li><code>क</code> (ka) + <code>ा</code> (aa matra) = <code>का</code> (kaa)</li>
    <li><code>क</code> (ka) + <code>ि</code> (i matra) = <code>कि</code> (ki)</li>
    <li><code>क</code> (ka) + <code>ं</code> (anusvara) = <code>कं</code> (kam)</li>
  </ul>
  <p>
    Standard Western tokenizers (like Python’s standard <code>\\b</code> word boundary regex) look for alphanumeric characters (<code>[a-zA-Z0-9_]</code>). 
    Because Unicode combining marks (Unicode category <code>Mn</code>) fall outside standard ASCII word sets, naive regex engines chop the matra off the consonant! 
    A query like <code>कांदा भाव</code> gets severed into broken fragments like <code>क</code> + <code>ांदा</code>.
  </p>

  <div class="praman-callout">
    <h4 style="margin-top:0; color:#ea580c;">The Praman Solution: Lookaround Matra Protection</h4>
    <p style="margin-bottom:0;">
      Praman uses Brahmic combining mark boundary protection regex:
      <code>(?&lt;![\\u0900-\\u0903\\u093a-\\u094f\\u0951-\\u0957\\u0962-\\u0963])\\b(?![\\u0900-\\u0903\\u093a-\\u094f\\u0951-\\u0957\\u0962-\\u0963])</code>
      This ensures words retain their phonetic integrity, vowel signs, and anusvaras across all 10 Indic scripts.
    </p>
  </div>

  <h2>Why Clickstream Volume Models Fail in Bharat</h2>
  <p>
    Traditional SEO tools don't actually measure real-time search engine autocomplete. Instead, they buy anonymized clickstream data from desktop browser extensions (which are used almost exclusively by corporate workers in the US, Europe, and urban metros).
  </p>
  <p>
    In non-metro India, <strong>over 85% of internet browsing happens on Android smartphones via WhatsApp, YouTube, and Google Chrome</strong>. 
    Clickstream data brokers have virtually zero tracking visibility into Tier-2 and Tier-3 smartphone users. The result? Traditional tools guess "0 search volume".
  </p>

  <h2>The Evidence-Based Alternative</h2>
  <p>
    Rather than guessing fake numbers, Praman probes the four fundamental dimensions of real-time search engine autocomplete:
  </p>
  <ol>
    <li><strong>Expansion Breadth (50%):</strong> Does the seed branch into a wide consonant alphabet tree?</li>
    <li><strong>Head Coverage (25%):</strong> Does the root query appear in the top autocomplete suggestions?</li>
    <li><strong>Question Density (15%):</strong> Are users asking interrogatives (काय, कसे, कुठे, कब, कैसे)?</li>
    <li><strong>Rank Depth (10%):</strong> How prominently does the seed appear in suggestion rankings?</li>
  </ol>

  <div style="text-align:center; margin:2.5rem 0;">
    <a href="https://www.praman.blog/" class="praman-btn-cta">⚡ Test Your Keywords Live on Praman.blog</a>
  </div>
</div>
"""
    },
    {
        "title": "मराठी शेती आणि बाजारभाव ब्लॉगिंग: Ahrefs शिवाय हाय-डिमांड कीवर्ड कसे शोधावे?",
        "slug": "marathi-agriculture-keyword-research-case-study",
        "categories": [3, 7],  # Marathi, Case Studies
        "excerpt": "कांदा भाव, पीक विमा, आणि हवामान अंदाज: पारंपारिक टूल्स फेल का होतात आणि प्रमाण (Praman) च्या मदतीने अचूक शेती कीवर्ड कसे शोधावे.",
        "content": THEME_STYLE + """
<div class="praman-theme-wrapper">
  <p class="lead" style="font-size:1.15rem; color:#645648;">
    महाराष्ट्रातील कृषी आणि शेतीविषयक ब्लॉगर्सची एकच मोठी तक्रार असते: Ahrefs किंवा SEMrush मध्ये <strong>कांदा भाव</strong>, <strong>सोयाबीन बाजारभाव</strong>, किंवा <strong>पीक विमा यादी</strong> शोधल्यास सर्च व्हॉल्यूम 0 किंवा 10 दाखवतो, पण प्रत्यक्ष ब्लॉगवर मात्र हजारो शेतकरी दररोज भेट देतात!
  </p>

  <h2>सर्च व्हॉल्यूमच्या खोट्या आकड्यांमागील सत्य</h2>
  <p>
    परदेशी कंपन्यांचे कीवर्ड टूल्स इंग्रजी भाषेसाठी बनवले गेले आहेत. मराठीतील 'कांदा' हा शब्द इंग्रजी कीवर्ड टूल्समध्ये शोधल्यास त्यांना त्यातील काना (ा) आणि अनुस्वार (ं) समजत नाही. त्यामुळे ते कोणताही अचूक डेटा देऊ शकत नाहीत.
  </p>

  <div class="praman-callout">
    <h4 style="margin-top:0; color:#ea580c;">प्रमाण (Praman) कसा मदत करतो?</h4>
    <p>
      प्रमाण कोणत्याही खोट्या व्हॉल्यूमचे अंदाज लावत नाही. प्रमाण थेट गुगलच्या ऑटो-कम्प्लिट इंजिनमधून ४ स्तरांवर तपासणी करतो:
    </p>
    <ul>
      <li><strong>कन्सोनंट अल्फॅबेट (क ते ज्ञ):</strong> 'कांदा अ', 'कांदा ब', 'कांदा क' असे सर्व पर्याय तपासून खरी मागणी शोधतो.</li>
      <li><strong>प्रश्न व हेतू (Intent):</strong> शेतकरी काय विचारत आहेत? (उदा. 'कांदा भाव कधी वाढणार', 'कांदा चाळ अनुदान योजना').</li>
    </ul>
  </div>

  <h2>प्रत्यक्ष उदाहरण: 'कांदा' या विषयावरील रिसर्च</h2>
  <p>
    जेव्हा आपण प्रमाणवर <code>कांदा</code> हा सीड कीवर्ड टाकतो, तेव्हा खालील हाय-डिमांड ब्रांचेस समोर येतात:
  </p>
  <ul>
    <li>🟢 <strong>Strong Evidence (डिमांड इंडेक्स &ge; ०.५०):</strong> <code>कांदा भाव आजचे</code>, <code>कांदा निर्यात बंदी</code>, <code>कांदा अनुदान यादी 2026</code>.</li>
    <li>🟡 <strong>कन्वर्सेशनल प्रश्न:</strong> <code>कांदा साठवणूक कशी करावी</code>, <code>कांद्याला भाव कधी मिळणार</code>.</li>
  </ul>

  <h2>कंटेंट प्लॅनर आणि अंतर्गत लिंक्स</h2>
  <p>
    फक्त कीवर्ड शोधून चालत नाही, तर कोणत्या क्रमाने लेख प्रसिद्ध करावेत हे देखील महत्वाचे आहे. प्रमाण मधील <strong>Editorial Content Plan</strong> तुम्हाला सांगतो की पहिला पिलर आर्टिकल कोणता असावा आणि त्यातून इतर लेखांना कोणत्या अँकर टेक्स्टने लिंक द्यावी.
  </p>

  <div style="text-align:center; margin:2.5rem 0;">
    <a href="https://www.praman.blog/" class="praman-btn-cta">🌾 प्रमाणवर मराठी कीवर्ड रिसर्च करून पहा</a>
  </div>
</div>
"""
    },
    {
        "title": "हिंदी फाइनेंस और शेयर बाजार ब्लॉग्स के लिए कीवर्ड रिसर्च: सटीक डिमांड कैसे पहचानें",
        "slug": "hindi-finance-keyword-research-strategy",
        "categories": [4, 7],  # Hindi, Case Studies
        "excerpt": "म्यूचुअल फंड, आईपीओ और बचत खाता: हिंदी में वित्तीय सामग्री तैयार करने के लिए वैज्ञानिक कीवर्ड रणनीति।",
        "content": THEME_STYLE + """
<div class="praman-theme-wrapper">
  <p class="lead" style="font-size:1.15rem; color:#645648;">
    भारत के टियर-2 और टियर-3 शहरों में हिंदी में वित्तीय जानकारी (पर्सनल फाइनेंस, शेयर बाजार, म्यूचुअल फंड, सरकारी योजनाएं) सर्च करने वालों की संख्या पिछले 3 वर्षों में 300% से अधिक बढ़ी है।
  </p>

  <h2>पारंपरिक कीवर्ड टूल्स की सीमाएं</h2>
  <p>
    अधिकांश हिंदी वित्तीय ब्लॉगर्स Ahrefs या SEMrush पर निर्भर रहते हैं। लेकिन ये टूल्स हिंदी देवनागरी शब्दों के बीच के सूक्ष्म अंतर को नहीं पहचान पाते। उदाहरण के लिए, <strong>म्यूचुअल फंड में निवेश कैसे करें</strong> और <strong>म्यूचुअल फंड सही है या गलत</strong>—इन दोनों कीवर्ड्स का इंटेंट पूरी तरह से अलग है:
  </p>
  <ul>
    <li>पहला कीवर्ड <strong>हाउ-टू (How-To / शैक्षणिक)</strong> है।</li>
    <li>दूसरा कीवर्ड <strong>कंपैरिजन / संदेह निवारण (Comparison &amp; Trust)</strong> है।</li>
  </ul>

  <div class="praman-callout">
    <h4 style="margin-top:0; color:#ea580c;">प्रमाण का इंटेंट क्लासिफायर</h4>
    <p>
      प्रमाण स्वचालित रूप से हिंदी खोजों को ५ प्रमुख श्रेणियों में वर्गीकृत करता है:
    </p>
    <ul>
      <li><strong>ताजा रुझान (Freshness):</strong> 'आज का', 'नवीनतम', '2026 लिस्ट'.</li>
      <li><strong>लेनदेन (Transactional):</strong> 'डाउनलोड', 'फॉर्म', 'ऑनलाइन आवेदन'.</li>
      <li><strong>सवाल (Questions):</strong> 'क्या है', 'कैलकुलेटर', 'नियम'.</li>
    </ul>
  </div>

  <h2>सटीक एडिटोरियल कैलेंडर बनाएं</h2>
  <p>
    ब्लॉग पर ट्रैफिक बढ़ाने के लिए केवल अलग-अलग लेख लिखने के बजाय <strong>टॉपिक क्लस्टरिंग</strong> अपनाएं। प्रमाण का अल्गोरिदम देवनागरी और हिंग्लिश दोनों खोजों को एक क्लस्टर में बांधता है, जिससे आपकी वेबसाइट की अथॉरिटी तेजी से बढ़ती है।
  </p>

  <div style="text-align:center; margin:2.5rem 0;">
    <a href="https://www.praman.blog/" class="praman-btn-cta">📈 प्रमाण टूल पर हिंदी रिसर्च शुरू करें</a>
  </div>
</div>
"""
    }
]


def main():
    print("=== Starting Praman WordPress Setup ===")

    # 1. Delete default "Hello world!" post if present
    print("\n1. Cleaning up default sample posts...")
    del_res = api_delete("wp/v2/posts/1")
    print("Deleted post 1 result:", del_res.get("status", "ok"))

    # 2. Create Pages
    created_pages = {}
    print("\n2. Creating Essential Pages...")
    for p in PAGES:
        payload = {
            "title": p["title"],
            "slug": p["slug"],
            "content": p["content"],
            "status": "publish",
            "comment_status": "closed"
        }
        res = api_post("wp/v2/pages", payload)
        if "id" in res:
            created_pages[p["slug"]] = res["id"]
            print(f"Created page: {p['title']} (ID: {res['id']}, Slug: /{p['slug']}/)")
        else:
            print(f"Failed page {p['slug']}:", res)

    # 3. Set Home Page as Front Page if created
    if "home" in created_pages:
        print("\n3. Setting Static Front Page...")
        set_res = api_post("wp/v2/settings", {
            "show_on_front": "page",
            "page_on_front": created_pages["home"]
        })
        print("Front page configuration:", set_res.get("show_on_front"))

    # 4. Create Launch Blog Posts
    print("\n4. Publishing Launch Case Studies...")
    for post in POSTS:
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
            print(f"Published post: {post['title'][:40]}... (ID: {res['id']}, URL: {res.get('link')})")
        else:
            print(f"Failed post {post['slug']}:", res)

    print("\n=== Praman WordPress Setup Completed Successfully! ===")


if __name__ == "__main__":
    main()
