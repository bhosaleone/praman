"""Praman Web Server: Supports both FastAPI and stdlib ThreadingHTTPServer.

Allows out-of-the-box local execution without external dependencies,
while maintaining full FastAPI/Uvicorn compatibility for production containers.
"""

import json
import logging
from pathlib import Path
import sys
from typing import Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from praman.competition import CompetitionIndex, SerpObservation, derive_competition_band
from praman.config import Mode, Settings
from praman.languages import LANGUAGES
from praman.pipeline import run_research
from praman.planner import generate_content_plan
from praman.report import render_csv_report, render_markdown_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("praman.web")

STATIC_DIR = PROJECT_ROOT / "web" / "static"
TEMPLATES_DIR = PROJECT_ROOT / "web" / "templates"


def _handle_research_request(payload: dict[str, Any]) -> dict[str, Any]:
    """Core logic for research request, shared across server implementations."""
    seeds = payload.get("seeds", [])
    if isinstance(seeds, str):
        seeds = [s.strip() for s in seeds.split(",") if s.strip()]

    language = payload.get("language", "mr")
    mode_str = payload.get("mode", "fixture")
    latin_expansion = bool(payload.get("latin_expansion", False))
    max_queries = payload.get("max_queries")
    if max_queries:
        max_queries = int(max_queries)

    settings = Settings(
        language=language,
        mode=Mode(mode_str),
        latin_expansion=latin_expansion,
        max_queries=max_queries,
    )

    # Process human SERP observations if provided in payload
    comp_idx = None
    serp_dict = payload.get("serp_observations", {})
    if serp_dict:
        obs_list = []
        for kw, obs in serp_dict.items():
            thin = obs.get("thin")
            weak = obs.get("weak")
            stale = obs.get("stale")
            notes = obs.get("notes", "")
            band, count = derive_competition_band(thin, weak, stale)
            obs_list.append(
                SerpObservation(
                    keyword=kw,
                    top_results_stale=stale,
                    thin_results=thin,
                    weak_domains=weak,
                    own_sites_ranking=None,
                    notes=notes,
                    band=band,
                    recorded_count=count,
                )
            )
        comp_idx = CompetitionIndex(obs_list)

    result = run_research(seeds, settings, comp_idx)
    content_plan = generate_content_plan(result.scores)

    return {
        "mode": settings.mode.value,
        "language": settings.language,
        "is_truncated": result.is_truncated,
        "not_asked_seeds": result.not_asked_seeds,
        "weights": result.weights.as_dict(),
        "keywords": [
            {
                "seed": s.seed,
                "demand": s.demand,
                "demand_complete": s.demand_complete,
                "measured_mass": s.measured_mass,
                "priority_band": s.priority_band,
                "evidence_band": s.evidence_band,
                "intent": s.intent.intent,
                "article_shape": s.intent.article_shape,
                "axes": s.raw_axes,
                "components": s.components,
                "competition": {
                    "band": s.competition.band if s.competition else None,
                    "recorded_count": s.competition.recorded_count if s.competition else 0,
                    "notes": s.competition.notes if s.competition else "",
                } if s.competition else None,
                "signals": {
                    "suggestions_seen": s.signals.suggestions_seen,
                    "breadth_comparable": s.signals.breadth_comparable,
                    "cross_script_split": s.signals.cross_script_split,
                    "script_affinity": s.signals.script_affinity,
                    "discovered": s.signals.discovered[:50],
                    "research_candidates": s.signals.research_candidates,
                    "raw_observations": s.signals.raw_observations,
                },
            }
            for s in result.scores
        ],
        "planner": {
            "calendar": [
                {
                    "topic_id": c.topic_id,
                    "primary_title": c.primary_title,
                    "cluster_demand": c.cluster_demand,
                    "primary_intent": c.primary_intent,
                    "article_shape": c.article_shape,
                    "recommended_publish_order": c.recommended_publish_order,
                }
                for c in content_plan.calendar
            ],
            "link_graph": [
                {
                    "source_topic": l.source_topic,
                    "target_topic": l.target_topic,
                    "anchor_text": l.anchor_text,
                    "rationale": l.rationale,
                }
                for l in content_plan.link_graph
            ],
            "orphan_topics": content_plan.orphan_topics,
        },
        "markdown_report": render_markdown_report(result, settings.mode),
        "csv_report": render_csv_report(result),
    }


# =====================================================================
# Dual Engine: FastAPI if available, Stdlib ThreadingHTTPServer fallback
# =====================================================================

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, HTMLResponse
    from fastapi.staticfiles import StaticFiles

    app = FastAPI(title="Praman API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def get_index() -> HTMLResponse:
        index_file = TEMPLATES_DIR / "index.html"
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())

    @app.get("/api/health")
    async def get_health() -> dict[str, str]:
        return {"status": "ok", "version": "0.1.0"}

    @app.get("/api/languages")
    async def get_languages() -> dict[str, Any]:
        return {
            code: {
                "name": spec.name,
                "native_name": spec.native_name,
                "script": spec.script,
            }
            for code, spec in LANGUAGES.items()
        }

    @app.post("/api/research")
    async def post_research(payload: dict[str, Any]) -> dict[str, Any]:
        try:
            return _handle_research_request(payload)
        except Exception as e:
            logger.exception("Error processing research request")
            raise HTTPException(status_code=500, detail=str(e))

except ImportError:
    # FastAPI is not installed: define app as None
    app = None


def run_stdlib_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Runs a pure Python stdlib HTTP server when FastAPI/Uvicorn are not installed."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    import mimetypes

    class PramanHTTPHandler(BaseHTTPRequestHandler):
        def _send_json(self, data: Any, status: int = 200) -> None:
            raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(raw)

        def do_OPTIONS(self) -> None:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def do_HEAD(self) -> None:
            if self.path in ("/", "/index.html"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
            elif self.path in ("/health", "/api/health"):
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
            else:
                self.send_response(200)
                self.end_headers()

        def do_GET(self) -> None:
            if self.path == "/" or self.path == "/index.html":
                index_path = TEMPLATES_DIR / "index.html"
                with open(index_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            elif self.path in ("/api/health", "/health"):
                self._send_json({"status": "ok", "version": "0.1.0"})
            elif self.path == "/api/languages":
                self._send_json({
                    code: {"name": spec.name, "native_name": spec.native_name, "script": spec.script}
                    for code, spec in LANGUAGES.items()
                })
            elif self.path in ("/USER_MANUAL.md", "/manual", "/user-manual"):
                manual_path = PROJECT_ROOT / "USER_MANUAL.md"
                if manual_path.exists():
                    with open(manual_path, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/markdown; charset=utf-8")
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_error(404, "User Manual not found")
            elif self.path in ("/LAUNCH_PITCH.md", "/pitch", "/launch-pitch"):
                pitch_path = PROJECT_ROOT / "LAUNCH_PITCH.md"
                if pitch_path.exists():
                    with open(pitch_path, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/markdown; charset=utf-8")
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_error(404, "Launch pitch not found")
            elif self.path.startswith("/static/"):
                rel_path = self.path[len("/static/"):]
                target_file = STATIC_DIR / rel_path
                if target_file.exists() and target_file.is_file():
                    mime, _ = mimetypes.guess_type(str(target_file))
                    with open(target_file, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", mime or "application/octet-stream")
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_error(404, "Static file not found")
            else:
                self.send_error(404, "Not found")

        def do_POST(self) -> None:
            if self.path == "/api/research":
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len).decode("utf-8")
                try:
                    payload = json.loads(body)
                    res = _handle_research_request(payload)
                    self._send_json(res)
                except Exception as e:
                    logger.exception("Error in POST /api/research")
                    self._send_json({"error": str(e)}, status=500)
            else:
                self.send_error(404, "Endpoint not found")

    server = ThreadingHTTPServer((host, port), PramanHTTPHandler)
    logger.info("Serving Praman dashboard on http://%s:%d (Stdlib Engine)", host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server.")
        server.server_close()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_stdlib_server(port=port)
