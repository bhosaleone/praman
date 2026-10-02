# Praman (प्रमाण) — Comprehensive User Manual & Flow of Operations

> **Official User Manual & Operational Blueprint for the Praman Indic & English Keyword Demand & Editorial Content Planning Platform.**

---

## Table of Contents
1. [Introduction & Core Philosophy](#1-introduction--core-philosophy)
2. [System Architecture & Quick Start](#2-system-architecture--quick-start)
3. [The Complete Flow of Operations (Step-by-Step)](#3-the-complete-flow-of-operations-step-by-step)
   - [Step 1: Language & Seed Configuration](#step-1-language--seed-configuration)
   - [Step 2: Selecting Execution Mode & Budget Options](#step-2-selecting-execution-mode--budget-options)
   - [Step 3: Running the Measurement Engine](#step-3-running-the-measurement-engine)
   - [Step 4: Interpreting the Demand Analysis Table](#step-4-interpreting-the-demand-analysis-table)
   - [Step 5: Verifying Mathematical Scores (Formula Modal)](#step-5-verifying-mathematical-scores-formula-modal)
   - [Step 6: Exploring the Scrollable Research Tree Canvas](#step-6-exploring-the-scrollable-research-tree-canvas)
   - [Step 7: The Active `[+ Measure]` Discovery Loop](#step-7-the-active--measure-discovery-loop)
   - [Step 8: Diagnosing Intent & Inspecting Evidence](#step-8-diagnosing-intent--inspecting-evidence)
   - [Step 9: Recording Human SERP Competition](#step-9-recording-human-serp-competition)
   - [Step 10: Editorial Content Calendar & Internal Linking](#step-10-editorial-content-calendar--internal-linking)
   - [Step 11: Exporting Reports (Markdown, CSV, JSON)](#step-11-exporting-reports-markdown-csv-json)
4. [The 4 Demand Axes & Mathematical Invariants](#4-the-4-demand-axes--mathematical-invariants)
5. [Evidence Banding Cheatsheet](#5-evidence-banding-cheatsheet)
6. [Troubleshooting & FAQs](#6-troubleshooting--faqs)

---

## 1. Introduction & Core Philosophy

**Praman** (प्रमाण) is an evidence-first keyword research and editorial planning tool engineered specifically for Indian regional languages and English.

### Why Traditional SEO Tools Fail You
Most global SEO suites (Ahrefs, Semrush, Google Keyword Planner) were built for Latin-alphabet search volumes derived from US/EU clickstream data. When applied to Indian regional languages:
- They return **"0 search volume"** or empty rows for queries searched by millions of regional users.
- They silently guess numbers or force English transliterations.
- They renormalize calculations, treating network failures or empty sets as "zero opportunity."

### The Praman Guarantees
1. **Refusal to Fake Volume**: Praman never fabricates search volume, estimated clicks, or automated difficulty scores.
2. **Missing Measurement Is Not Zero**: Praman uses a strict 3-state codomain ($V = \mathbb{R} \cup \{\bot\}$):
   - **Measured Absence ($0.0$)**: Google returned an empty suggestion list.
   - **Unmeasured ($\bot$)**: The probe failed due to network timeout or rate-limiting. It is excluded from the denominator, not coerced to zero.
   - **Never Asked ($\bot$)**: The query budget ceiling was hit before this query could be issued.
3. **Transparent Pinned Weights**: Scores are completely explainable and reproducible:
   $$\text{demand}(s) = 0.50 \cdot \text{breadth}(s) + 0.25 \cdot \text{coverage}(s) + 0.15 \cdot \text{density}(s) + 0.10 \cdot \text{depth}(s)$$
4. **Linguistic Precision**: Native awareness of Brahmic combining matras, SOV (Subject-Object-Verb) question grammar, and bilingual topic grouping.

---

## 2. System Architecture & Quick Start

### Running Locally
Praman is built with a zero-dependency Python standard library core, with an optional FastAPI/Uvicorn server for production containers.

1. **Launch the Dashboard**:
   ```bash
   cd /home/shrikant/Desktop/app/praman
   python3 web/app.py 8000
   ```
2. **Access in Browser**:
   Open `http://localhost:8000` in any modern web browser (Firefox, Chrome, Edge, Safari).
3. **Verify Health**:
   ```bash
   curl -s http://localhost:8000/health
   # Returns: {"status": "ok", "version": "0.1.0"}
   ```

---

## 3. The Complete Flow of Operations (Step-by-Step)

```
[Input Seeds & Language]
          ↓
[Choose Mode: Fixture / Live / Recorded]
          ↓
[Click 'Run Measurement Loop']
          ↓
[Demand Table Analysis] ──┬─→ [Score Pill: View Formula Breakdown]
                          ├─→ [Intent Badge: Inspect Suggestion Evidence]
                          ├─→ ['Review' Button: Record Human SERP Competition]
                          ├─→ ['Tree' Button: Scrollable Research Tree Canvas]
                          │         ↓
                          │   [Click '+ Measure' on Candidates] ──┐
                          │         ↓                             │
                          │   [Active Measurement Loop] ←─────────┘
                          │
                          ├─→ [Editorial Planner: Calendar & Link Graph]
                          └─→ [Export: Markdown, CSV, JSON Reports]
```

---

### Step 1: Language & Seed Configuration

1. **Choose Your Target Language**:
   Use the language dropdown to select from **11 supported languages**:
   - Marathi (`mr`), Hindi (`hi`), Tamil (`ta`), Telugu (`te`), Bengali (`bn`), Gujarati (`gu`), Kannada (`kn`), Malayalam (`ml`), Punjabi (`pa`), Odia (`or`), or English (`en`).
2. **Input Seed Keywords**:
   Type or paste your root topics separated by commas or new lines. For example:
   ```text
   शेती, हवामान, पीक विमा, marathi sheti
   ```
3. **Quick Presets**:
   Click any of the curated preset buttons to instantly populate seeds:
   - `🌾 Marathi Agri`: `शेती, हवामान, पीक विमा, marathi sheti`
   - `🇮🇳 Hindi Tech`: `मोबाइल, लैपटॉप, सरकारी योजना, आधार कार्ड`
   - `🌴 Tamil Schemes`: `விவசாயம், பயிர் காப்பீடு, வானிலை, மின்சார மானியம்`
   - `🌐 English Agri`: `crop insurance, agriculture scheme, weather forecast, tractor subsidy`

---

### Step 2: Selecting Execution Mode & Budget Options

Expand **Advanced Configuration & Mode Controls** to customize the run:

| Mode | Best For | Behavior |
|---|---|---|
| **Fixture (Default)** | Offline testing, UI demo, development | Generates deterministic, mathematically compliant mock autocomplete suggestions without external network calls. |
| **Live** | Real-world production research | Queries Google Autocomplete in real-time using polite request pacing. |
| **Recorded** | Deterministic audit, CI/CD, team sharing | Uses content-addressed local snapshot fixtures from previous runs. |

#### Additional Toggles
- **Cross-Script Latin Expansion**: Check this box if your seed is in an Indic script (e.g. `शेती`) and you want Praman to also probe English letters (`a-z`) for bilingual Romanised queries (e.g. `sheti yojana`).
- **Query Budget Ceiling**: Limits the maximum number of network probes per run (e.g. `200`) to prevent IP rate-limiting on large seed batches.

---

### Step 3: Running the Measurement Engine

Click the primary action button:
$$\mathbf{[🚀\text{ Run Measurement Loop}]}$$

#### What Happens Under the Hood
1. **Deterministic Expansion**:
   - **Head Query**: Probes the root seed itself (e.g. `पीक विमा`).
   - **Alphabet Probes**: Probes the seed combined with each native consonant in strict alphabetical order (e.g. `पीक विमा क`, `पीक विमा ख`...).
   - **Modifier Probes**: Probes intent templates (e.g. `online`, `pdf`, `2026`, `योजना`).
   - **SOV Question Probes**: Injects natural interrogatives based on the language's syntax (e.g. `पीक विमा काय`, `पीक विमा किती`).
2. **Quality Filtering**:
   - Raw probe strings (like `पीक विमा क`) are classified into **Raw Autocomplete Observations**.
   - Clean, multi-word terms (like `पीक विमा किती`, `पीक विमा 2026`) are elevated into **Research Candidates**.
3. **Signal Calculation & Pinned Scoring**:
   - Calculates Breadth, Coverage, Density, and Depth.
   - Pinned formula evaluates the Demand Index and determines the **Evidence Band**.

---

### Step 4: Interpreting the Demand Analysis Table

The primary dashboard table displays the core evaluation for every seed:

| Column | What It Means | How to Interpret |
|---|---|---|
| **Seed Keyword** | The analyzed root phrase | Formatted in monospace code. |
| **Demand Index** | Combined score ($0.000$ to $1.000$) | Displayed as a colored pill. A `⚠️` flag denotes a partial score where some voice was unmeasured. |
| **Evidence Band** | Autocomplete evidence strength | `Strong` ($\ge 0.50$), `Moderate` ($0.25–0.49$), `Weak` ($< 0.25$), or `Insufficient` (Unmeasured). |
| **Intent** | Inferred linguistic intent | `informational`, `transactional`, `howto`, `freshness`, `comparison`, or `unclear 🔍`. |
| **Breadth (50%)** | Fraction of alphabet expansions yielding suggestions | Measures broad market awareness. Shows `⚠` if truncated. |
| **Coverage (25%)** | Head query presence | $1.0$ if head query autocompletes; $0.0$ if empty. |
| **Density (15%)** | Proportion of suggestions containing question markers | Direct signal of problem-solving user curiosity. |
| **Depth (10%)** | Suggestion list ranking position | $1.0 / \text{rank}$ if seed appears in top-10 autocomplete list. |
| **Competition** | Human SERP qualitative band | `Low`, `Medium`, `High`, or `unmeasured`. Click `📝 Review` to edit. |
| **Research Tree** | Tree inspector trigger | Shows candidate count. Click to open the tree canvas. |

---

### Step 5: Verifying Mathematical Scores (Formula Modal)

Click on any **Demand Score Pill** (e.g. `0.875` or `0.844`) in the table to open the **Demand Score Explanation Modal**:

```
┌────────────────────────────────────────────────────────┐
│  Demand Score Breakdown: "शेती"                        │
├─────────────┬───────────┬──────────────┬───────────────┤
│ Voice       │ Weight    │ Raw Value    │ Component     │
├─────────────┼───────────┼──────────────┼───────────────┤
│ Breadth     │ 50.0%     │ 1.000        │ +0.500        │
│ Coverage    │ 25.0%     │ 1.000        │ +0.250        │
│ Density     │ 15.0%     │ 0.167        │ +0.025        │
│ Depth       │ 10.0%     │ 1.000        │ +0.100        │
├─────────────┼───────────┼──────────────┼───────────────┤
│ TOTAL       │ 100.0%    │ c(s) = 1.000 │ 0.875         │
└─────────────┴───────────┴──────────────┴───────────────┘
Status: Complete Measurement (Theorem 1)
Evidence Band: Strong Evidence (Demand ≥ 0.50)
```

- This ensures full reproducibility: you can hand this formula breakdown to any editor, client, or stakeholder to defend why an article topic was prioritized.

---

### Step 6: Exploring the Scrollable Research Tree Canvas

Click the **`🌳 Research Tree`** tab in the main navigation (or click the `🌳 Tree (81)` button in any table row):

1. **Tree Canvas Controls**:
   - 🔍 **Filter Candidate Tree**: Type any word (e.g. `2026` or `pdf`) to instantly highlight matching branches.
   - 🌱 **Seed Dropdown**: Switch between viewing all seeds simultaneously or isolating a specific seed.
   - 📂 **Expand All / Collapse All**: Toggle nested raw observations.
2. **Contained Scrollbars**:
   - The tree canvas viewport is pinned to `max-height: 580px;` with both vertical and horizontal scrollbars.
   - Candidates are neatly partitioned:
     - 🎯 **Research Candidates**: Clean, high-value keyword targets with `[+ Measure]` buttons.
     - 📜 **Raw Observations**: Collapsible details container preserving consonant probe artifacts for auditability.

---

### Step 7: The Active `[+ Measure]` Discovery Loop

This is Praman's primary engine for editorial ideation:

1. Browse candidates discovered around your root seed (e.g. around `पीक विमा`, you discover `पीक विमा किती`).
2. Click **`[+ Measure]`** directly on the candidate card.
3. Praman automatically:
   - Adds `पीक विमा किती` to your active seed inputs.
   - Triggers an immediate research cycle.
   - Evaluates the child query across its own 4 axes and discovers tertiary candidates.
4. **Result**: You transform a single general seed into an entire cluster of 20–30 interlinked, validated article opportunities.

---

### Step 8: Diagnosing Intent & Inspecting Evidence

When a seed query lacks explicit question words or transaction tokens (e.g. `शेती` or `crop insurance`), Praman labels its intent as **`unclear 🔍`**.

#### Why `unclear` is a Feature, Not a Failure
Praman's methodology dictates that intent must be derived from verifiable linguistic markers. Silently coercing every keyword to "informational" is deceptive.

#### Using the Intent Diagnostic Modal
Click on the **`unclear 🔍`** badge to open the **Intent Diagnostic & Suggestion Evidence Modal**:
1. **Diagnostic Explanation**: Explains why the root seed has no grammatical intent marker.
2. **Scrollable Suggestion Evidence Pool**: Displays all expansion queries categorized into 5 intent buckets:
   - 📅 **Freshness Demand**: Queries seeking recent updates (e.g. `शेती 2026`).
   - 💳 **Transactional / Download Demand**: Queries seeking forms/PDFs (e.g. `शेती online`, `शेती pdf`).
   - 🛠️ **How-To / Process Queries**: Queries seeking guides (e.g. `शेती कशी करायची`).
   - ❓ **Questions / Informational**: Definition queries (e.g. `शेती काय आहे`).
   - ⚖️ **Comparison Demand**: Comparison queries (e.g. `शेती vs नोकरी`).
3. Click `[+ Measure]` on any intent candidate to immediately investigate that specific intent cluster.

---

### Step 9: Recording Human SERP Competition

Praman refuses to scrape Google SERP HTML (preventing IP blacklisting and ToS violations). Instead, it uses **Human-in-the-Loop qualitative observations**:

1. In the Demand Table, click **`📝 Review`** next to any seed.
2. Open a separate browser tab, search the seed on Google, and review the top-10 results.
3. In the modal, answer the **3 tri-state questions** (`Yes` / `Unrecorded` / `No`):
   - *Are weak/forum domains ranking in the top 5?* (Quora, Reddit, Facebook groups, personal blogs).
   - *Are top results thin or low effort?* (Short paragraphs, machine translations, generic aggregators).
   - *Are top results stale or outdated?* (Articles published > 2 years ago without updates).
4. **Derived Competition Band Rule**:
   - **Low Competition**: Weak domains present (`Yes`) **AND** thin content present (`Yes`).
   - **Medium Competition**: Weak domains present (`Yes`) **OR** stale content present (`Yes`).
   - **High Competition**: High-authority, comprehensive, fresh incumbents dominate (`No` to all).
   - **Unmeasured**: Less than 2 questions recorded.
5. Click **Apply Observations** to lock in the competition score.

---

### Step 10: Editorial Content Calendar & Internal Linking

Click the **`📅 Editorial Content Plan & Links`** tab to view your operational publishing roadmap:

#### 1. Content Calendar
- **Bilingual Clustering**: Uses Brahmic consonant skeleton keying (`topic_key`) to merge bilingual variations (e.g. `मराठी शेती` and `marathi sheti`) into a single editorial cluster.
- **Priority Publishing Order**: Ranks topics by cluster demand and intent specificity.
- **Recommended Article Shape**:
  - `Explainer`: Conceptual foundations.
  - `Guide`: Comprehensive step-by-step walkthroughs.
  - `Comparison`: Side-by-side product or scheme analysis.
  - `News / Update`: Fast-turnaround freshness content.

#### 2. Cycle-Free Internal Linking Graph
- Directs how each published article should link to other articles on your domain.
- Specifies exact **Source Topic $\to$ Target Topic**, recommended **Anchor Text**, and architectural **Rationale** (e.g. *Hub-to-Spoke*, *Topical Parent*, *Sibling Reference*).

---

### Step 11: Exporting Reports (Markdown, CSV, JSON)

Praman provides comprehensive export actions in the action bar:

- **👁️ Preview Report**: Opens an in-app viewer to preview the complete analysis report.
- **📄 Download Report (.md)**: Generates a publication-grade GitHub-Flavored Markdown report with executive summary, tables, and content calendar.
- **📊 Export CSV**: Exports the full keyword metrics table ready for Google Sheets or Microsoft Excel.
- **📦 Export JSON**: Exports the full structured data payload for integration into headless CMS systems, Notion, or automated publishing workflows.

---

## 4. The 4 Demand Axes & Mathematical Invariants

| Axis | Formula | Nominal Weight | Physical Meaning |
|---|---|:---:|---|
| **Breadth** | $\frac{\lvert\{e \in \text{Exp}(s) : \text{suggestions}(e) \neq \emptyset\}\rvert}{\lvert\text{Exp}(s)\rvert}$ | **50%** | The fraction of consonant and modifier probes that successfully return search suggestions. Measures total surface area of public demand. |
| **Coverage** | $1.0 \text{ if } \lvert\text{head}(s)\rvert > 0 \text{ else } 0.0$ | **25%** | Verifies that the head query itself triggers Google autocomplete. |
| **Density** | $\frac{\lvert\{u \in U(s) : \text{is\_question}(u)\}\rvert}{\lvert U(s)\rvert}$ | **15%** | Proportion of discovered suggestions that represent explicit questions. High density denotes intense informational problem-solving intent. |
| **Depth** | $\frac{1}{\text{rank}(s)}$ | **10%** | Position of the seed within Google's ranked autocomplete suggestions. Google ranks top suggestions by relative query frequency. |

---

## 5. Evidence Banding Cheatsheet

| Evidence Band | Demand Score Range | Editorial Recommendation |
|---|:---:|---|
| 🟢 **Strong Evidence** | $\ge 0.50$ | **Immediate Priority**: Broad autocomplete footprint, heavy user questioning, and top rank positions. Create comprehensive pillar content. |
| 🟡 **Moderate Evidence** | $0.25 - 0.49$ | **Secondary Priority**: Solid presence on partial expansion axes. Good target for supporting cluster articles. |
| ⚪ **Weak Evidence** | $< 0.25$ | **Opportunistic**: Niche, emerging, or ultra-long-tail topic. Write only if competition is verified Low. |
| 🔴 **Insufficient Evidence** | $\bot$ (`None`) | **Do Not Rank**: Network or budget failure prevented measurement. Never treat as zero; re-run when connectivity improves. |

---

## 6. Troubleshooting & FAQs

### Q: Why do all my seeds show "Strong Evidence"?
**A**: Broad root queries (e.g. `शेती`, `हवामान`, `पीक विमा`) have massive statewide demand that triggers suggestions on almost every consonant probe. To test long-tail gaps, test targeted queries like `सोयाबीन तणनाशक फवारणी वेळ` or `ठिबक सिंचन अनुदान योजना 2026`.

### Q: Why are some candidates labeled "Raw Observations"?
**A**: When probing consonants (e.g. `पीक विमा` + `क`), Google autocomplete might echo the probe string `पीक विमा क`. Praman filters out single trailing consonants and orphan probe letters into "Raw Observations" so your content calendar only contains clean, grammatically natural search phrases.

### Q: What should I do if a seed shows "⚠️ Partial"?
**A**: A `⚠️` indicates that at least one voice (e.g. Depth or Coverage) could not be measured. Praman refuses to renormalize surviving weights; the measured mass $c(s) < 1.0$ caps the achievable score. Check your network connection or verify that the seed query was not rate-limited.

### Q: Does Praman support English queries?
**A**: Yes! Praman fully supports English (`en`) with Latin alphabet expansion (`a-z`), SVO question syntax (`what is`, `how to`, `why`, `price`), and English modifier templates.
