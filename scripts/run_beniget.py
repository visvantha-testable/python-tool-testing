"""Beniget def-use chain analysis for sample_subject/src Python files."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sample_subject" / "src"
OUT = ROOT / "reports" / "beniget_defuse.json"

try:
    from beniget import DefUseChains
    import gast as ast
except ImportError:
    print(json.dumps({"error": "beniget or gast not installed"}))
    sys.exit(0)

results = {}
for pyfile in sorted(SRC.glob("*.py")):
    src_text = pyfile.read_text(encoding="utf-8")
    try:
        module = ast.parse(src_text)
        duc = DefUseChains()
        duc.visit(module)
        results[str(pyfile.relative_to(ROOT))] = {
            "chains_count": len(duc.chains),
            "file": str(pyfile.relative_to(ROOT)),
        }
    except Exception as exc:
        results[str(pyfile.relative_to(ROOT))] = {"error": str(exc)}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
