# Praman — System Architecture & Deployment Specification

**Praman** (प्रमाण — *evidence, proof; that by which a thing is established*) is a keyword demand research and editorial content planning application for Indian regional languages.

It builds directly upon the principles, empirical findings, and mathematical specifications established in:
- `NO_API.md`: Refusal to fake unauthenticated metrics (volume, CPC, automated difficulty).
- `METHODOLOGY.md`: The measurement contract, three-state codomain, and failure representations.
- `MATH.md`: The formal algebraic specification of the pinned demand blend, Theorems 1–4, and truncation bounds.
- `PRIOR_ART_KD_FORMULAS.md`: Evidence that commercial difficulty metrics are black boxes requiring private backlink indexes, validating human-observed SERP notes.
- `product/`: Generalisation to 10 Indic languages with an editorial content planner as the moat.

---

## 1. Architectural Guardrails

### 1.1 The Three-State Codomain
Every observable value takes values in $V = \mathbb{R} \cup \{\bot\}$:
1. **Measured Absence ($0.0$)**: Google Autocomplete returned HTTP 200 with an empty list `[]`. Demand was looked for and not found.
2. **Unmeasured ($\bot$ / `None`)**: A network timeout, HTTP error, consent wall, or unparseable payload occurred. Excluded from ranking; never converted to $0.0$.
3. **Never Asked ($\bot$ / `None`)**: The query or seed budget ceiling (`--max-seeds`, `--max-queries`) cut off execution prior to issuance. Flagged and reported separately.

### 1.2 Pinned Demand Blend
The demand score is a convex combination of four measured voices:
$$\text{demand}(s) = \sum_{i \in A(s)} W_i \cdot v_i(s)$$
Where:
- $W = \{\text{breadth}: 0.50, \text{coverage}: 0.25, \text{density}: 0.15, \text{depth}: 0.10\}$
- $A(s) = \{ i : v_i(s) \neq \bot \}$
- The denominator does **not** move. Unmeasured voices are not redistributed.
- Measured mass $c(s) = \sum_{i \in A(s)} W_i$. When $c(s) < 1.0$, `demand_complete = False` and the score is capped below 1.0.

### 1.3 Human-Recorded Competition (Weight 0)
- Human observation flags: `thin_results`, `weak_domains`, `top_results_stale` (yes/no/blank).
- Blank values in CSV are parsed as `None` (unrecorded), never `False`.
- Requires $\ge 2$ observed fields to assign a band (`low`, `medium`, `high`, `very_high`).

---

## 2. Indic Linguistic Engine

### 2.1 Brahmic Word Boundary & Combining Marks
Standard Python regex `\b` fails across Brahmic scripts because matras, viramas (halant/pulli), and dependent vowels are classified as combining marks. Praman implements a custom regex generator and tokenizer in `praman.script` ensuring boundaries do not match inside words.

### 2.2 Cross-Script Topic Identity
Audience queries often mix Devanagari/native script and Latin transliteration (e.g. `मराठी शेती` and `marathi sheti`). `topic_key` extracts a lossy consonant skeleton, clustering these queries into a single editorial target without conflating alphabet expansion queries.

---

## 3. Deployment Structure

The entire application is organized in a self-contained layout:
- `praman/`: Pure Python 3.10+ standard library core engine.
- `cli.py`: Standalone CLI supporting offline recorded playback, fixture mode, and live requests.
- `web/`: Lightweight Web dashboard (FastAPI/Uvicorn) with visual charts, link graph exploration, and SERP note taking.
- `Dockerfile` & `docker-compose.yml`: Containerized setup ready for single-container deployment (Render, Railway, VPS, or local Docker).
