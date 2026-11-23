"""Zip src/urqse into docs/py/urqse.zip for Pyodide. Deterministic: sorted entries, fixed
timestamps and permissions, .py files only, so an unchanged package gives a byte-identical zip.
urqse/data (the offline build, which needs pandas/rasterio) is left out: the browser never uses it."""

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "docs" / "py" / "urqse.zip"
EPOCH = (1980, 1, 1, 0, 0, 0)
EXCLUDE = ("__pycache__", "data")  # path parts under src/urqse never shipped


def build(out: Path = OUT) -> Path:
    pkg = SRC / "urqse"
    files = sorted(p for p in pkg.rglob("*.py") if not set(p.relative_to(pkg).parts) & set(EXCLUDE))
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".zip.tmp")
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(SRC).as_posix(), date_time=EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    tmp.replace(out)
    return out


if __name__ == "__main__":
    path = build(Path(sys.argv[1]) if len(sys.argv) > 1 else OUT)
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")
