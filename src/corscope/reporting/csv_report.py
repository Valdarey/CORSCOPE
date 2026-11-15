"""CSV findings report writer."""
import csv
from pathlib import Path

def write_csv(data: dict, path: str | Path) -> Path:
    output=Path(path); output.parent.mkdir(parents=True,exist_ok=True)
    fields=["severity","title","description","risk_explanation","recommendation","confidence","verified_vulnerability"]
    with output.open("w",newline="",encoding="utf-8") as handle:
        writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader()
        for finding in data.get("findings",[]): writer.writerow({k:finding.get(k,"") for k in fields})
    return output
