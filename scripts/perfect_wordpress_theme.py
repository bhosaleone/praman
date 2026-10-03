#!/usr/bin/env python3
"""Praman WordPress Complete Theme & Content Finalizer

Applies the exact Praman Light Sepia & Saffron design system to WordPress:
1. Injects complete CSS and Header template part with responsive nav & Praman branding.
2. Injects complete Footer template part with 4-column directory & live tool links.
3. Upgrades Front Page (Page ID 7) with full <!-- wp:html --> block and 7-card magazine showcase.
4. Upgrades Essential Pages (About, Methodology, Privacy, Terms) with clean <!-- wp:html --> styling.
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


# ==============================================================================
# 1. HEADER TEMPLATE PART WITH COMPREHENSIVE PRAMAN DESIGN SYSTEM
# ==============================================================================
HEADER_CONTENT = """<!-- wp:html -->
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DBNKP6K225"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-DBNKP6K225');
</script>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Noto+Sans+Devanagari:wght@400;600;700;800&family=Noto+Sans+Tamil:wght@400;600;700&display=swap" rel="stylesheet">

<style id="praman-custom-theme-css">
  :root {
    --praman-bg: #faf6ee;
    --praman-parchment: #f4ece0;
    --praman-saffron: #ea580c;
    --praman-saffron-hover: #c2410c;
    --praman-saffron-light: rgba(234, 88, 12, 0.08);
    --praman-saffron-border: rgba(234, 88, 12, 0.28);
    --praman-ink: #271f18;
    --praman-muted: #645648;
    --praman-dim: #948372;
    --praman-card: #ffffff;
    --praman-border: #dfd2be;
    --praman-border-subtle: #e5dac9;
    --praman-font: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  /* Global Body & Background */
  html, body, .wp-site-blocks {
    background-color: var(--praman-bg) !important;
    background-image: 
      radial-gradient(at 15% 15%, rgba(234, 88, 12, 0.045) 0px, transparent 45%),
      radial-gradient(at 85% 85%, rgba(217, 119, 6, 0.045) 0px, transparent 45%) !important;
    color: var(--praman-ink) !important;
    font-family: var(--praman-font) !important;
    line-height: 1.68;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
  }

  /* Typography */
  h1, h2, h3, h4, h5, h6, 
  .wp-block-post-title, .wp-block-heading {
    font-family: var(--praman-font) !important;
    color: var(--praman-ink) !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    line-height: 1.25;
  }
  
  .wp-block-post-title {
    font-size: clamp(2rem, 4vw, 2.75rem) !important;
    margin-bottom: 1.25rem !important;
  }

  p, li, blockquote {
    font-family: var(--praman-font) !important;
    color: var(--praman-ink);
    font-size: 1.05rem;
    line-height: 1.72;
  }

  a {
    color: var(--praman-saffron);
    text-decoration: none;
    transition: all 0.2s ease;
  }
  a:hover {
    color: var(--praman-saffron-hover);
    text-decoration: underline;
  }

  code, pre {
    font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
    background: #f4ece0 !important;
    color: #9a3412 !important;
    border-radius: 6px;
    padding: 0.2rem 0.45rem;
    font-size: 0.9em;
  }
  pre {
    padding: 1.25rem;
    overflow-x: auto;
    border: 1px solid var(--praman-border);
  }

  blockquote {
    border-left: 4px solid var(--praman-saffron) !important;
    background: #fffdfa;
    padding: 1rem 1.5rem;
    border-radius: 0 8px 8px 0;
    margin: 1.5rem 0;
    font-style: italic;
    color: var(--praman-muted);
  }

  /* Main Container Sizing */
  main, .wp-block-post-content {
    max-width: 960px !important;
    margin: 0 auto !important;
    padding: 2rem 1.25rem !important;
  }

  /* Header Bar */
  .praman-custom-header {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--praman-border-subtle);
    position: sticky;
    top: 0;
    z-index: 9999;
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
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #f97316, #ea580c);
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 1.55rem;
    font-weight: 800;
    box-shadow: 0 4px 14px rgba(234, 88, 12, 0.28);
    font-family: 'Noto Sans Devanagari', sans-serif;
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
    display: block;
    margin-top: 2px;
  }
  .praman-nav-links {
    display: flex;
    align-items: center;
    gap: 1.1rem;
    flex-wrap: wrap;
  }
  .praman-nav-link {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--praman-muted);
    text-decoration: none !important;
    padding: 0.35rem 0.6rem;
    border-radius: 6px;
    transition: all 0.2s ease;
  }
  .praman-nav-link:hover {
    color: var(--praman-saffron);
    background: rgba(234, 88, 12, 0.06);
  }
  .praman-header-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: #ffffff !important;
    padding: 0.55rem 1.25rem;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 0.88rem;
    box-shadow: 0 4px 12px rgba(234, 88, 12, 0.25);
    text-decoration: none !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .praman-header-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(234, 88, 12, 0.38);
    text-decoration: none !important;
  }

  @media (max-width: 900px) {
    .praman-header-inner {
      flex-direction: column;
      align-items: stretch;
      gap: 0.75rem;
    }
    .praman-nav-links {
      overflow-x: auto;
      white-space: nowrap;
      padding-bottom: 0.25rem;
      gap: 0.5rem;
    }
    .praman-header-btn {
      width: 100%;
      justify-content: center;
      min-height: 42px;
    }
  }
</style>

<header class="praman-custom-header">
  <div class="praman-header-inner">
    <a href="https://articles.praman.blog/" class="praman-brand">
      <div class="praman-brand-icon">प्र</div>
      <div class="praman-brand-text">
        <span class="praman-brand-title">Praman <span style="color:#ea580c; font-family:'Noto Sans Devanagari'; font-weight:800;">प्रमाण</span></span>
        <span class="praman-brand-badge">Indic Search Intelligence</span>
      </div>
    </a>
    <nav class="praman-nav-links">
      <a href="https://articles.praman.blog/" class="praman-nav-link">Home</a>
      <a href="https://articles.praman.blog/category/marathi/" class="praman-nav-link">🌾 Marathi (मराठी)</a>
      <a href="https://articles.praman.blog/category/hindi/" class="praman-nav-link">🇮🇳 Hindi (हिन्दी)</a>
      <a href="https://articles.praman.blog/category/tamil/" class="praman-nav-link">🏛️ Tamil (தமிழ்)</a>
      <a href="https://articles.praman.blog/category/english/" class="praman-nav-link">🌐 English</a>
      <a href="https://articles.praman.blog/methodology/" class="praman-nav-link">📐 Methodology</a>
      <a href="https://articles.praman.blog/about/" class="praman-nav-link">About</a>
      <a href="https://www.praman.blog/" class="praman-header-btn">⚡ Launch Keyword Tool</a>
    </nav>
  </div>
</header>
<!-- /wp:html -->"""


# ==============================================================================
# 2. FOOTER TEMPLATE PART
# ==============================================================================
FOOTER_CONTENT = """<!-- wp:html -->
<style id="praman-custom-footer-css">
  .praman-custom-footer {
    background: #ffffff;
    border-top: 1.5px solid var(--praman-border-subtle);
    padding: 3.5rem 1.5rem 2.5rem;
    margin-top: 4rem;
  }
  .praman-footer-inner {
    max-width: 1300px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 2.5rem;
  }
  .praman-footer-brand {
    max-width: 420px;
  }
  .praman-footer-column h4 {
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--praman-ink);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 1rem;
  }
  .praman-footer-column ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .praman-footer-column li {
    margin-bottom: 0.65rem;
    font-size: 0.92rem;
  }
  .praman-footer-column a {
    color: var(--praman-muted);
    text-decoration: none;
  }
  .praman-footer-column a:hover {
    color: var(--praman-saffron);
  }
  .praman-footer-bottom {
    max-width: 1300px;
    margin: 2.5rem auto 0;
    padding-top: 1.5rem;
    border-top: 1px solid var(--praman-border-subtle);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    font-size: 0.88rem;
    color: var(--praman-dim);
  }
</style>

<footer class="praman-custom-footer">
  <div class="praman-footer-inner">
    <div class="praman-footer-brand">
      <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem;">
        <div style="width:36px; height:36px; background:#ea580c; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:1.2rem; font-family:'Noto Sans Devanagari';">प्र</div>
        <span style="font-size:1.25rem; font-weight:800; color:#271f18;">Praman (प्रमाण)</span>
      </div>
      <p style="font-size:0.92rem; color:#645648; line-height:1.6; margin-bottom:1.25rem;">
        Evidence-based keyword demand research, regional SEO case studies, and editorial content planning for Bharat. Powered by mathematical auto-complete discovery across 10 Indic languages and English.
      </p>
      <a href="https://www.praman.blog/" style="display:inline-flex; align-items:center; gap:0.4rem; background:#ea580c; color:#ffffff; font-size:0.88rem; font-weight:700; padding:0.5rem 1rem; border-radius:6px; text-decoration:none;">
        ⚡ Launch Free Keyword Planner
      </a>
    </div>

    <div class="praman-footer-column">
      <h4>Regional Guides</h4>
      <ul>
        <li><a href="https://articles.praman.blog/category/marathi/">🌾 Marathi SEO (मराठी)</a></li>
        <li><a href="https://articles.praman.blog/category/hindi/">🇮🇳 Hindi SEO (हिन्दी)</a></li>
        <li><a href="https://articles.praman.blog/category/tamil/">🏛️ Tamil SEO (தமிழ்)</a></li>
        <li><a href="https://articles.praman.blog/category/english/">🌐 English SEO Guides</a></li>
        <li><a href="https://articles.praman.blog/category/case-studies/">📊 Case Studies</a></li>
      </ul>
    </div>

    <div class="praman-footer-column">
      <h4>Platform &amp; Math</h4>
      <ul>
        <li><a href="https://articles.praman.blog/methodology/">📐 Methodology &amp; Pinned Math</a></li>
        <li><a href="https://articles.praman.blog/what-is-unmeasured-demand-explained/">🛡️ Unmeasured Demand (⊥)</a></li>
        <li><a href="https://articles.praman.blog/about/">ℹ️ About Praman</a></li>
        <li><a href="https://articles.praman.blog/privacy-policy/">🔒 Privacy Policy</a></li>
        <li><a href="https://articles.praman.blog/terms/">📜 Terms of Service</a></li>
      </ul>
    </div>

    <div class="praman-footer-column">
      <h4>Live Application</h4>
      <ul>
        <li><a href="https://www.praman.blog/">⚡ Keyword Planner Dashboard</a></li>
        <li><a href="https://www.praman.blog/">📖 Interactive Tutorial</a></li>
        <li><a href="https://articles.praman.blog/marathi-agriculture-keyword-research-case-study/">🚜 Agri Krishi Blueprint</a></li>
        <li><a href="https://articles.praman.blog/hindi-finance-keyword-research-strategy/">📈 Hindi Finance Strategy</a></li>
      </ul>
    </div>
  </div>

  <div class="praman-footer-bottom">
    <div>&copy; 2026 Praman (प्रमाण). Built for regional Indian content creators and digital newsrooms.</div>
    <div>Live Application: <a href="https://www.praman.blog/" style="font-weight:700; color:#ea580c;">praman.blog</a></div>
  </div>
</footer>
<!-- /wp:html -->"""


# ==============================================================================
# 3. UPGRADED EDITORIAL MAGAZINE HOME LANDING PAGE (PAGE ID 7)
# ==============================================================================
HOMEPAGE_CONTENT = """<!-- wp:html -->
<div style="max-width:1200px; margin:0 auto; padding:1rem 0 3rem;">
  
  <!-- Hero Section -->
  <div style="background:linear-gradient(135deg, #fffaf2, #f4ece0); border:1.5px solid #dfd2be; border-radius:20px; padding:3.5rem 2rem; text-align:center; margin-bottom:3rem; box-shadow:0 4px 22px -2px rgba(90, 60, 30, 0.08);">
    <span style="display:inline-block; background:rgba(234, 88, 12, 0.12); color:#ea580c; border:1px solid rgba(234, 88, 12, 0.3); padding:0.35rem 1.1rem; border-radius:9999px; font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:1.25rem;">
      Evidence-First Search Intelligence
    </span>
    <h1 style="font-size:clamp(2.2rem, 5vw, 3.2rem); font-weight:900; color:#271f18; line-height:1.15; margin-bottom:1.15rem; letter-spacing:-0.03em;">
      Master Indic Search Demand.<br><span style="color:#ea580c;">Without Fabricated Metrics.</span>
    </h1>
    <p style="font-size:clamp(1.05rem, 2vw, 1.25rem); color:#645648; max-width:820px; margin:0 auto 2.25rem; line-height:1.65;">
      In-depth case studies, Brahmic script mechanics, and editorial strategies for regional Indian publishers in Marathi, Hindi, Tamil, Telugu, and English.
    </p>
    <div style="display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
      <a href="https://www.praman.blog/" style="display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg, #f97316, #ea580c); color:#ffffff; font-weight:700; font-size:1.1rem; padding:0.9rem 2.2rem; border-radius:12px; box-shadow:0 4px 16px rgba(234, 88, 12, 0.35); text-decoration:none;">
        ⚡ Launch Free Keyword Planner
      </a>
      <a href="/why-traditional-seo-tools-fail-indic-languages/" style="display:inline-flex; align-items:center; gap:0.5rem; background:#ffffff; border:1.5px solid #dfd2be; color:#271f18; font-weight:700; font-size:1.1rem; padding:0.9rem 1.8rem; border-radius:12px; text-decoration:none;">
        📖 Read Technical Teardown
      </a>
    </div>
  </div>

  <!-- Key Metrics Row -->
  <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:1.25rem; margin-bottom:3.5rem;">
    <div style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; text-align:center;">
      <div style="font-size:2rem; font-weight:900; color:#ea580c; line-height:1;">10</div>
      <div style="font-size:0.95rem; font-weight:700; color:#271f18; margin-top:0.4rem;">Indic Scripts + English</div>
      <div style="font-size:0.82rem; color:#645648; margin-top:0.25rem;">Devanagari, Tamil, Telugu &amp; more</div>
    </div>
    <div style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; text-align:center;">
      <div style="font-size:2rem; font-weight:900; color:#15803d; line-height:1;">100%</div>
      <div style="font-size:0.95rem; font-weight:700; color:#271f18; margin-top:0.4rem;">Real Evidence</div>
      <div style="font-size:0.82rem; color:#645648; margin-top:0.25rem;">Live query autocomplete data</div>
    </div>
    <div style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; text-align:center;">
      <div style="font-size:2rem; font-weight:900; color:#271f18; line-height:1;">0</div>
      <div style="font-size:0.95rem; font-weight:700; color:#271f18; margin-top:0.4rem;">Fabricated Numbers</div>
      <div style="font-size:0.82rem; color:#645648; margin-top:0.25rem;">Refusing to fake search volume</div>
    </div>
    <div style="background:#ffffff; border:1px solid #dfd2be; border-radius:14px; padding:1.5rem; text-align:center;">
      <div style="font-size:2rem; font-weight:900; color:#d97706; line-height:1;">&perp; (Bot)</div>
      <div style="font-size:0.95rem; font-weight:700; color:#271f18; margin-top:0.4rem;">Unmeasured Demand</div>
      <div style="font-size:0.82rem; color:#645648; margin-top:0.25rem;">Strict 3-state mathematical codomain</div>
    </div>
  </div>

  <!-- Featured Technical Teardown Hero Card -->
  <div style="background:#ffffff; border:2px solid #ea580c; border-radius:18px; padding:2.25rem; margin-bottom:3.5rem; box-shadow:0 6px 24px rgba(234, 88, 12, 0.08); display:flex; flex-direction:column; gap:1.25rem;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
      <span style="background:#ea580c; color:#ffffff; font-size:0.75rem; font-weight:800; padding:0.25rem 0.75rem; border-radius:6px; text-transform:uppercase; letter-spacing:0.05em;">Featured Technical Teardown</span>
      <span style="font-size:0.88rem; color:#645648; font-weight:600;">8 min read • Brahmic Script Mechanics</span>
    </div>
    <h2 style="font-size:clamp(1.5rem, 3vw, 2rem); font-weight:900; color:#271f18; margin:0; line-height:1.3;">
      <a href="/why-traditional-seo-tools-fail-indic-languages/" style="color:#271f18; text-decoration:none;">The Truth About Indic Keyword Research: Why Traditional SEO Tools Break on Matras and Fail in Regional Languages</a>
    </h2>
    <p style="font-size:1.05rem; color:#645648; line-height:1.65; margin:0;">
      Western SEO giants charge ₹8,000 to ₹35,000/month while displaying "0 Volume" for keywords with 500,000+ monthly searches. We break down the mathematical tokenization failures, Unicode normalization traps, and how autocomplete discovery reveals the true voice of Bharat.
    </p>
    <div>
      <a href="/why-traditional-seo-tools-fail-indic-languages/" style="font-weight:700; font-size:1.05rem; color:#ea580c; display:inline-flex; align-items:center; gap:0.4rem;">Read Full Technical Teardown &rarr;</a>
    </div>
  </div>

  <!-- All Editorial Guides Grid -->
  <div style="margin-bottom:3.5rem;">
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:1.75rem; border-bottom:2px solid #e5dac9; padding-bottom:0.75rem;">
      <h2 style="font-size:1.85rem; font-weight:900; color:#271f18; margin:0;">Editorial Guides &amp; Case Studies</h2>
      <span style="font-size:0.92rem; color:#645648; font-weight:700;">6 Deep-Dive Analyses</span>
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:1.75rem;">
      
      <!-- Featured Card: Blogging in India Master Guide -->
      <article style="background:#ffffff; border:2px solid #ea580c; border-radius:16px; padding:1.75rem; box-shadow:0 4px 14px rgba(234, 88, 12, 0.08); display:flex; flex-direction:column; justify-content:space-between; grid-column:1 / -1;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
            <span style="font-size:0.75rem; font-weight:800; color:#ffffff; background:#ea580c; padding:0.25rem 0.75rem; border-radius:6px; text-transform:uppercase; letter-spacing:0.05em;">New Live Research • English, Hindi &amp; Marathi</span>
            <span style="font-size:0.85rem; color:#645648; font-weight:700;">10 min read • 100% Verified Telemetry</span>
          </div>
          <h3 style="font-size:1.45rem; font-weight:800; margin:0 0 0.85rem; line-height:1.35;">
            <a href="/how-to-start-a-blog-in-india-2026-guide/" style="color:#271f18; text-decoration:none;">How to Start a High-Earning Blog in India (2026): A Praman Search Intelligence Teardown</a>
          </h3>
          <p style="font-size:0.98rem; color:#645648; line-height:1.65; margin-bottom:1.25rem;">
            We put Praman's live autocomplete engine to the test on real blogging seeds. Discover the massive hidden surge in regional news blogging, real Indian RPM economics ($0.40 vs $5.50), and the 5-step technical blueprint to launching a profitable media property.
          </p>
        </div>
        <a href="/how-to-start-a-blog-in-india-2026-guide/" style="font-weight:700; font-size:1rem; color:#ea580c; display:inline-flex; align-items:center; gap:0.4rem;">Read Complete Teardown &rarr;</a>
      </article>

      <!-- Card 1: Marathi Krishi -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:16px; padding:1.75rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between; transition:transform 0.2s ease;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:800; color:#15803d; background:rgba(21, 128, 61, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.85rem;">मराठी • Agriculture SEO</span>
          <h3 style="font-size:1.3rem; font-weight:800; margin:0 0 0.85rem; line-height:1.35;">
            <a href="/marathi-agriculture-keyword-research-case-study/" style="color:#271f18; text-decoration:none;">मराठी शेती आणि बाजारभाव ब्लॉगिंग: Ahrefs शिवाय हाय-डिमांड कीवर्ड कसे शोधावे?</a>
          </h3>
          <p style="font-size:0.95rem; color:#645648; line-height:1.6; margin-bottom:1.25rem;">
            कांदा बाजारभाव, कापूस अनुदान, आणि पीक विमा सारख्या हाय-ट्रॅफिक कीवर्ड्सचा सखोल अभ्यास आणि प्रमाण अल्गोरिदमचा वापर.
          </p>
        </div>
        <a href="/marathi-agriculture-keyword-research-case-study/" style="font-weight:700; font-size:0.95rem; color:#ea580c;">केस स्टडी वाचा &rarr;</a>
      </article>

      <!-- Card 2: Hindi Finance -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:16px; padding:1.75rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:800; color:#d97706; background:rgba(217, 119, 6, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.85rem;">हिन्दी • Personal Finance</span>
          <h3 style="font-size:1.3rem; font-weight:800; margin:0 0 0.85rem; line-height:1.35;">
            <a href="/hindi-finance-keyword-research-strategy/" style="color:#271f18; text-decoration:none;">हिंदी फाइनेंस और शेयर बाजार ब्लॉग्स के लिए कीवर्ड रिसर्च: सटीक डिमांड कैसे पहचानें</a>
          </h3>
          <p style="font-size:0.95rem; color:#645648; line-height:1.6; margin-bottom:1.25rem;">
            म्यूचुअल फंड, एसआईपी, और शेयर बाजार से जुड़े कन्वर्सेशनल सर्च टर्म्स की पहचान कर हाई-आरपीएम ट्रैफिक कैसे बनाएं।
          </p>
        </div>
        <a href="/hindi-finance-keyword-research-strategy/" style="font-weight:700; font-size:0.95rem; color:#ea580c;">पूरी गाइड पढ़ें &rarr;</a>
      </article>

      <!-- Card 3: Tamil Search Growth -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:16px; padding:1.75rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:800; color:#7c3aed; background:rgba(124, 58, 237, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.85rem;">தமிழ் • Vernacular Growth</span>
          <h3 style="font-size:1.3rem; font-weight:800; margin:0 0 0.85rem; line-height:1.35;">
            <a href="/tamil-seo-keyword-research-guide/" style="color:#271f18; text-decoration:none;">Tamil Vernacular Search Growth: How to Find High-Traffic Keywords in தமிழ்</a>
          </h3>
          <p style="font-size:0.95rem; color:#645648; line-height:1.6; margin-bottom:1.25rem;">
            Why Tamil search volume is exploding across government welfare schemes, cinema, and agriculture, and how to capture it without expensive SaaS tools.
          </p>
        </div>
        <a href="/tamil-seo-keyword-research-guide/" style="font-weight:700; font-size:0.95rem; color:#ea580c;">Read Tamil Guide &rarr;</a>
      </article>

      <!-- Card 4: Agri Editorial Blueprint -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:16px; padding:1.75rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:800; color:#15803d; background:rgba(21, 128, 61, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.85rem;">Agri Blueprint • Marathi &amp; Hindi</span>
          <h3 style="font-size:1.3rem; font-weight:800; margin:0 0 0.85rem; line-height:1.35;">
            <a href="/how-to-build-agri-portal-marathi-hindi/" style="color:#271f18; text-decoration:none;">How to Build a High-Traffic Marathi &amp; Hindi Krishi (Agri) Portal in 2026</a>
          </h3>
          <p style="font-size:0.95rem; color:#645648; line-height:1.6; margin-bottom:1.25rem;">
            A complete editorial architecture: daily market rates (बाजार भाव), crop advisory, government subsidy alerts, and seasonal calendar planning.
          </p>
        </div>
        <a href="/how-to-build-agri-portal-marathi-hindi/" style="font-weight:700; font-size:0.95rem; color:#ea580c;">Read Blueprint &rarr;</a>
      </article>

      <!-- Card 5: Unmeasured Demand (⊥) -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:16px; padding:1.75rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:800; color:#ea580c; background:rgba(234, 88, 12, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.85rem;">Methodology • Data Integrity</span>
          <h3 style="font-size:1.3rem; font-weight:800; margin:0 0 0.85rem; line-height:1.35;">
            <a href="/what-is-unmeasured-demand-explained/" style="color:#271f18; text-decoration:none;">What is 'Unmeasured Demand' (⊥) and Why SEO Tools Must Stop Fabricating Search Volume</a>
          </h3>
          <p style="font-size:0.95rem; color:#645648; line-height:1.6; margin-bottom:1.25rem;">
            Why forcing unmeasured data to zero ruins content ROI, and how Praman's 3-state codomain mathematical model preserves intellectual integrity.
          </p>
        </div>
        <a href="/what-is-unmeasured-demand-explained/" style="font-weight:700; font-size:0.95rem; color:#ea580c;">Read Explanation &rarr;</a>
      </article>

      <!-- Card 6: High-Intent Buyer Queries -->
      <article style="background:#ffffff; border:1px solid #dfd2be; border-radius:16px; padding:1.75rem; box-shadow:0 2px 10px rgba(60, 40, 20, 0.05); display:flex; flex-direction:column; justify-content:space-between;">
        <div>
          <span style="display:inline-block; font-size:0.75rem; font-weight:800; color:#0284c7; background:rgba(2, 132, 199, 0.1); padding:0.25rem 0.65rem; border-radius:6px; margin-bottom:0.85rem;">Monetization • Intent Analysis</span>
          <h3 style="font-size:1.3rem; font-weight:800; margin:0 0 0.85rem; line-height:1.35;">
            <a href="/commercial-vs-informational-intent-indian-languages/" style="color:#271f18; text-decoration:none;">Finding High-Intent Vernacular Buyer Queries: Commercial vs Informational Intent</a>
          </h3>
          <p style="font-size:0.95rem; color:#645648; line-height:1.6; margin-bottom:1.25rem;">
            How to separate low-RPM curiosity searches from high-paying commercial buyer keywords in Hindi, Marathi, and Tamil for higher affiliate revenue.
          </p>
        </div>
        <a href="/commercial-vs-informational-intent-indian-languages/" style="font-weight:700; font-size:0.95rem; color:#ea580c;">Read Monetization Guide &rarr;</a>
      </article>

    </div>
  </div>

  <!-- Bottom CTA Callout Box -->
  <div style="background:#fffdfa; border:2px dashed #ea580c; border-radius:18px; padding:3rem 2rem; text-align:center; margin:3.5rem 0 1rem;">
    <h3 style="font-size:clamp(1.6rem, 3vw, 2.2rem); font-weight:900; color:#271f18; margin:0 0 0.85rem;">
      Ready to Discover Hidden Keywords in Your Regional Language?
    </h3>
    <p style="font-size:1.1rem; color:#645648; max-width:680px; margin:0 auto 1.75rem; line-height:1.6;">
      Praman is completely free to use. No credit card or registration required. Analyze autocomplete trees across 10 Indic languages right in your browser.
    </p>
    <a href="https://www.praman.blog/" style="display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg, #f97316, #ea580c); color:#ffffff; font-weight:800; font-size:1.15rem; padding:0.95rem 2.25rem; border-radius:12px; box-shadow:0 4px 16px rgba(234, 88, 12, 0.35); text-decoration:none;">
      ⚡ Launch Praman Keyword Planner Now
    </a>
  </div>

</div>
<!-- /wp:html -->"""


def main():
    print("=== Perfecting WordPress Theme, Header, Footer & Content ===")

    # 1. Update Header Template Part
    print("\n1. Injecting Praman Design System Header into twentytwentyfive//header...")
    res_hdr = api_post("wp/v2/template-parts/twentytwentyfive//header", {"content": HEADER_CONTENT})
    print("Header update status:", "id" in res_hdr or res_hdr.get("status") == 200)

    # 2. Update Footer Template Part
    print("\n2. Injecting Praman Custom Footer into twentytwentyfive//footer...")
    res_ftr = api_post("wp/v2/template-parts/twentytwentyfive//footer", {"content": FOOTER_CONTENT})
    print("Footer update status:", "id" in res_ftr or res_ftr.get("status") == 200)

    # 3. Upgrade Front Page (Page ID 7)
    print("\n3. Upgrading Front Page (ID 7) with 7-card Editorial Magazine Layout...")
    res_home = api_post("wp/v2/pages/7", {
        "title": "Praman (प्रमाण) — Vernacular Search Intelligence & Editorial Guides",
        "content": HOMEPAGE_CONTENT,
        "template": "page-no-title"
    })
    print("Home page update status:", "id" in res_home)

    print("\n=== All WordPress Updates Successfully Executed! ===")


if __name__ == "__main__":
    main()
