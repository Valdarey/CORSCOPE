"""JSON report writer."""
import json
from pathlib import Path

def write_json(data: dict, path: str | Path) -> Path:
    output=Path(path); output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
    return output
