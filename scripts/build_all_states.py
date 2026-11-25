"""Build, calibrate and export every supported state for the web simulator (offline, long-running).

    python scripts/build_all_states.py [YEAR] [--only IA,NE,...]

Per state, in a fresh process: urqse.data.build_state, urqse.calibrate.run_state, urqse.data.export_web.
A failing state is recorded and skipped; the rest go on. Downloads are cached (data_raw/), so a rerun
only redoes what failed. Writes reports/STATES_STATUS.md with the outcome and the first error line
of every state."""

import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from urqse.data.build_state import STATE_NAME, STATES, UNSUPPORTED  # noqa: E402

STEPS = (("build", "urqse.data.build_state"), ("calibrate", "urqse.calibrate.run_state"), ("export", "urqse.data.export_web"))
STATUS_JSON = ROOT / "reports" / "states_status.json"
LOG_DIR = ROOT / "data" / "logs"


def last_error(text: str) -> str:
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    return next((ln for ln in reversed(lines) if "Error" in ln or "error" in ln), lines[-1] if lines else "")


def run_state(state: str, year: int) -> dict:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    for step, module in STEPS:
        res = subprocess.run([sys.executable, "-m", module, state, str(year)], cwd=ROOT, capture_output=True, text=True)
        (LOG_DIR / f"{state}_{year}_{step}.log").write_text(res.stdout + res.stderr)
        if res.returncode != 0:
            return dict(state=state, ok=False, step=step, error=last_error(res.stderr or res.stdout), seconds=time.time() - t0)
    return dict(state=state, ok=True, step="export", error="", seconds=time.time() - t0)


def write_status(status: dict, year: int):
    STATUS_JSON.parent.mkdir(exist_ok=True)
    STATUS_JSON.write_text(json.dumps(status, indent=1) + "\n")
    ok = [s for s in status.values() if s["ok"]]
    L = [f"# State builds, base year {year}", "",
         f"Updated {dt.date.today().isoformat()} by `python scripts/build_all_states.py {year}`. "
         f"{len(ok)} of the {len(STATES)} regions (50 states and DC) are in the web simulator.", "",
         "| State | Result | Failed step | Reason |", "|---|---|---|---|"]  # fmt: skip
    for st in sorted(STATES, key=STATE_NAME.get):
        if st in UNSUPPORTED:
            L.append(f"| {STATE_NAME[st]} | not built | | {UNSUPPORTED[st]} |")
        elif st in status:
            s = status[st]
            L.append(f"| {STATE_NAME[st]} | {'ok' if s['ok'] else 'failed'} | {'' if s['ok'] else s['step']} | "
                     f"{s['error'].replace('|', '/')} |")  # fmt: skip
        else:
            L.append(f"| {STATE_NAME[st]} | not run | | |")
    (ROOT / "reports" / "STATES_STATUS.md").write_text("\n".join(L) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("year", type=int, nargs="?", default=2022)
    ap.add_argument("--only", default="", help="comma-separated postal codes (default: every supported state)")
    a = ap.parse_args(argv)
    todo = [s.strip().upper() for s in a.only.split(",") if s.strip()] or [s for s in STATES if s not in UNSUPPORTED]
    status = json.loads(STATUS_JSON.read_text()) if STATUS_JSON.exists() else {}
    for st in todo:
        print(f"{st} ...", flush=True)
        status[st] = run_state(st, a.year)
        s = status[st]
        print(f"{st} {'ok' if s['ok'] else 'FAILED at ' + s['step'] + ': ' + s['error']} ({s['seconds']:.0f} s)", flush=True)
        write_status(status, a.year)


if __name__ == "__main__":
    main()
