"""Evaluation harness: runs baseline and agent solution over the same cases,
scores both with the independent auditor, and writes the results table the
brief asks for (eval/results/summary.json + summary.md).

Usage (from repo root, ANTHROPIC_API_KEY set):
    python eval/run_eval.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from eval.audit import audit_script  # noqa: E402
from src.baseline import BaselineAgent  # noqa: E402
from src.pipeline import run_agent_pipeline  # noqa: E402

CASES_DIR = REPO_ROOT / "eval" / "cases"
RESULTS_DIR = REPO_ROOT / "eval" / "results"


def load_cases() -> list[tuple[str, str]]:
    cases = []
    for path in sorted(CASES_DIR.glob("*.txt")):
        cases.append((path.stem, path.read_text(encoding="utf-8")))
    return cases


def run_case(case_id: str, source_text: str) -> dict:
    result = {"case_id": case_id}

    t0 = time.time()
    baseline_script = BaselineAgent().run(case_id, source_text)
    baseline_time = time.time() - t0
    baseline_audit = audit_script(source_text, baseline_script)

    t0 = time.time()
    ledger, verified = run_agent_pipeline(case_id, source_text)
    agent_time = time.time() - t0
    agent_audit = audit_script(
        source_text,
        verified.script,
        rendered_only_scene_ids={s.scene_id for s in verified.renderable_scenes},
    )

    result["baseline"] = {
        "accuracy": baseline_audit.accuracy,
        "total_factual": baseline_audit.total_factual,
        "supported_factual": baseline_audit.supported_factual,
        "runtime_s": round(baseline_time, 2),
    }
    result["agent"] = {
        "accuracy": agent_audit.accuracy,
        "total_factual": agent_audit.total_factual,
        "supported_factual": agent_audit.supported_factual,
        "runtime_s": round(agent_time, 2),
        "scenes_total": len(verified.script.scenes),
        "scenes_blocked": len(verified.blocked_scene_ids),
        "blocked_detail": [
            {"scene_id": v.scene_id, "status": v.status, "detail": v.detail}
            for v in verified.verdicts
            if v.status != "verified"
        ],
        "source_conflicts_detected": len(ledger.conflicts),
    }
    return result


def main() -> None:
    cases = load_cases()
    if not cases:
        print(f"No cases found in {CASES_DIR} (expecting .txt files). Nothing to run.")
        return

    all_results = [run_case(case_id, text) for case_id, text in cases]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "summary.json").write_text(
        json.dumps(all_results, indent=2), encoding="utf-8"
    )

    n = len(all_results)
    avg_baseline = sum(r["baseline"]["accuracy"] for r in all_results) / n
    avg_agent = sum(r["agent"]["accuracy"] for r in all_results) / n
    total_blocked = sum(r["agent"]["scenes_blocked"] for r in all_results)

    lines = [
        "# Evaluation summary",
        "",
        f"Cases: {n}",
        "",
        "| Metric | Simple baseline | Agent solution | Change |",
        "|---|---|---|---|",
        f"| Source-grounded claim accuracy | {avg_baseline:.0%} | {avg_agent:.0%} | "
        f"{avg_agent - avg_baseline:+.0%} |",
        f"| Scenes blocked by verification (total) | 0 | {total_blocked} | — |",
        "",
        "Per-case detail in `summary.json`.",
    ]
    (RESULTS_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
