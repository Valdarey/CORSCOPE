"""Self-contained HTML report writer."""
import html, json
from pathlib import Path

def write_html(data: dict, path: str | Path) -> Path:
    output=Path(path); output.parent.mkdir(parents=True,exist_ok=True)
    findings=[]
    for f in data.get("findings",[]):
        findings.append("<section><h2>"+html.escape(str(f.get("severity")))+" — "+html.escape(str(f.get("title")))+"</h2>"
          +"<p>"+html.escape(str(f.get("description")))+"</p><h3>Evidence</h3><pre>"+
          html.escape(json.dumps(f.get("evidence"),indent=2,ensure_ascii=False))+"</pre><h3>Recommendation</h3><p>"+
          html.escape(str(f.get("recommendation")))+"</p></section>")
    body="".join(findings) or "<p>No findings.</p>"
    document="<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>CORSCOPE report</title><style>body{font:16px system-ui;max-width:1000px;margin:2rem auto;padding:0 1rem;color:#202124}section{border:1px solid #ddd;border-radius:8px;padding:1rem;margin:1rem 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f5f5;padding:1rem}small{color:#555}</style><h1>CORSCOPE Assessment Report</h1><p><b>Target:</b> "+html.escape(str(data.get("target")))+"</p><p><b>Timestamp:</b> "+html.escape(str(data.get("timestamp")))+"</p>"+body+"<h2>Limitations</h2><ul>"+"".join("<li>"+html.escape(str(x))+"</li>" for x in data.get("limitations",[]))+"</ul></html>"
    output.write_text(document,encoding="utf-8"); return output
