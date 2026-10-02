# Praman (प्रमाण)

> **Evidence-first keyword demand research and content planning for Indian regional languages.**
> Refusing to fake numbers. Missing measurement is not zero.

---

## What Praman Does

1. **Relative Demand Measurement**: Quantifies Google Autocomplete demand across 10 Indic languages (`mr`, `hi`, `bn`, `te`, `ta`, `gu`, `kn`, `ml`, `pa`, `or`) without an Ads account.
2. **Pinned-Weight Demand Blend**: Evaluates Expansion Breadth ($0.50$), Coverage ($0.25$), Question Density ($0.15$), and Rank Depth ($0.10$). Unmeasured axes never distort surviving weights.
3. **Intent & Outline Mapping**: Classifies intent (Informational, How-to, Transactional, Navigational, Freshness, Comparison) based on Indic syntax and generates article outlines.
4. **Editorial Content Planner**: Clusters cross-script duplicates (e.g. `मराठी शेती` and `marathi sheti`), generates publication priorities, and produces an internal-link graph with exact anchor recommendations.
5. **Human SERP Notes**: Tracks real human SERP observations (`thin_results`, `weak_domains`, `top_results_stale`) without scraping or proxy guessing.

---

## Quickstart

### 1. Standalone CLI (Zero Dependencies)
Run offline using synthetic fixtures or recorded replays:

```bash
# Offline demo run using synthetic fixtures
python3 cli.py research "शेती" "हवामान" --lang mr --mode fixture

# Generate human SERP review CSV template
python3 cli.py serp "शेती" "हवामान" -o observations.csv

# Score research with human competition notes
python3 cli.py research "शेती" "हवामान" --lang mr --serp observations.csv --out report.md

# Generate content planning & internal link graph
python3 cli.py plan "शेती" "हवामान" --lang mr --out content_plan.md
```

### 2. Web Dashboard
Start the visual dashboard:

```bash
pip install -r requirements.txt
uvicorn web.app:app --reload --port 8000
```
Open [http://localhost:8000](http://localhost:8000).

### 3. Docker Deployment
```bash
docker compose up --build
```
Access at `http://localhost:8000`.

---

## Running Verification Tests
```bash
python3 -m unittest discover -s tests
```
Asserts mathematical consistency, combining mark regex accuracy, and Theorem 1–4 bounds.
