"""CORSCOPE command-line interface."""
import json, logging
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from corscope import __version__
from corscope.config import ScanConfig
from corscope.core.engine import AssessmentEngine
from corscope.core.http_client import HTTPClient
from corscope.core.validator import validate_target, InvalidTargetError
from corscope.modules.origin import analyze_origins
from corscope.modules.headers import inspect_headers
from corscope.modules.credentials import analyze_credentials
from corscope.modules.preflight import analyze_preflight
from corscope.reporting.json_report import write_json
from corscope.reporting.csv_report import write_csv
from corscope.reporting.html_report import write_html
from corscope.utils.helpers import default_report_path

app=typer.Typer(help="CORSCOPE — Modular CORS Security Assessment Tool",no_args_is_help=True,invoke_without_command=True)
console=Console()

def _client(timeout: float, delay: float, verify_tls: bool, follow_redirects: bool) -> HTTPClient:
    return HTTPClient(ScanConfig(timeout=timeout,delay=delay,verify_tls=verify_tls,follow_redirects=follow_redirects))

def _run(target: str, modules: set[str], output: str | None, report: str | None,
         timeout: float, delay: float, verify_tls: bool, follow_redirects: bool, verbose: bool=False):
    try: target=validate_target(target)
    except InvalidTargetError as exc: raise typer.BadParameter(str(exc)) from exc
    if verbose: logging.basicConfig(level=logging.DEBUG)
    console.print(f"[bold cyan]CORSCOPE v{__version__}[/bold cyan] — CORS Security Assessment")
    console.print(f"[green][+][/green] Target: {target}")
    client=_client(timeout,delay,verify_tls,follow_redirects)
    try:
        if modules=={"all"}:
            data=AssessmentEngine(client).scan(target)
        else:
            from datetime import datetime, timezone
            from corscope import __version__
            data={"target":target,"timestamp":datetime.now(timezone.utc).isoformat(),
                  "corscope_version":__version__,"findings":[],
                  "limitations":["Module-specific assessment; findings require contextual validation.",
                                 "No browser-based CORS enforcement or sensitive-data access was verified."]}
            if "origin" in modules:
                data["origin_analysis"]=analyze_origins(client,target)
                data["credential_analysis"]=analyze_credentials(data["origin_analysis"])
            if "headers" in modules:
                baseline=client.request("GET",target)
                data["http"]={"status_code":baseline.status_code,"headers":baseline.headers,
                              "elapsed_ms":round(baseline.elapsed_ms,2),"error":baseline.error}
                data["header_inspection"]=inspect_headers(baseline)
            if "preflight" in modules:
                data["preflight_analysis"]=analyze_preflight(client,target)
        table=Table(title="Risk Summary"); table.add_column("Severity"); table.add_column("Findings",justify="right")
        for severity in ["Critical","High","Medium","Low","Informational"]:
            count=sum(1 for f in data.get("findings",[]) if f.get("severity")==severity)
            if count: table.add_row(severity,str(count))
        console.print(table)
        if output:
            fmt=output.lower()
            if fmt not in {"json","csv","html"}: raise typer.BadParameter("Output must be json, csv, or html.")
            path=Path(report) if report else default_report_path(fmt)
            writers={"json":write_json,"csv":write_csv,"html":write_html}
            saved=writers[fmt](data,path); console.print(f"[green][+][/green] Report saved: {saved}")
        else:
            for finding in data.get("findings",[]):
                console.print(f"[{finding['severity']}] {finding['title']}")
            console.print("[dim]Use --output json|csv|html to save a report.[/dim]")
        console.print("[green][+][/green] Assessment completed. Header-based assessment only; no exploit verification performed.")
    finally: client.close()

@app.callback()
def main(version: bool = typer.Option(False, "--version", help="Show installed version.", is_eager=True)):
    """CORSCOPE CLI."""
    if version:
        console.print(f"CORSCOPE {__version__}")
        raise typer.Exit()

@app.command()
def scan(target: str=typer.Argument(...,help="Absolute HTTP(S) target URL"),
         output: str|None=typer.Option(None,"--output","-o",help="Report format: json, csv, html"),
         report: str|None=typer.Option(None,"--report",help="Report file path"),
         timeout: float=typer.Option(10.0,"--timeout",min=0.1,max=120),
         delay: float=typer.Option(0.0,"--delay",min=0,max=60),
         verify_tls: bool=typer.Option(True,"--verify-tls/--no-verify-tls"),
         follow_redirects: bool=typer.Option(False,"--follow-redirects/--no-follow-redirects"),
         verbose: bool=typer.Option(False,"--verbose","-v")):
    """Run the complete CORS assessment."""
    _run(target,{"all"},output,report,timeout,delay,verify_tls,follow_redirects,verbose)

@app.command()
def origin(target: str=typer.Argument(...), output: str|None=typer.Option(None,"--output"), report: str|None=typer.Option(None,"--report"), timeout: float=typer.Option(10.0,"--timeout")):
    """Run Origin Analyzer."""
    _run(target,{"origin"},output,report,timeout,0,True,False)

@app.command()
def headers(target: str=typer.Argument(...), output: str|None=typer.Option(None,"--output"), report: str|None=typer.Option(None,"--report"), timeout: float=typer.Option(10.0,"--timeout")):
    """Run Header Inspector."""
    _run(target,{"headers"},output,report,timeout,0,True,False)

@app.command()
def preflight(target: str=typer.Argument(...), output: str|None=typer.Option(None,"--output"), report: str|None=typer.Option(None,"--report"), timeout: float=typer.Option(10.0,"--timeout")):
    """Run Preflight Analyzer."""
    _run(target,{"preflight"},output,report,timeout,0,True,False)

@app.command("report")
def report_command(source: Path=typer.Argument(...,exists=True,readable=True), output: str=typer.Option("html","--output","-o"), report: Path|None=typer.Option(None,"--report")):
    """Convert an existing CORSCOPE JSON report to another format."""
    try: data=json.loads(source.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise typer.BadParameter(f"Cannot read JSON report: {exc}") from exc
    fmt=output.lower()
    if fmt not in {"json","csv","html"}: raise typer.BadParameter("Output must be json, csv, or html.")
    destination=report or default_report_path(fmt)
    {"json":write_json,"csv":write_csv,"html":write_html}[fmt](data,destination)
    console.print(f"[green][+][/green] Report saved: {destination}")

@app.command()
def config():
    """Display effective default configuration."""
    console.print_json(json.dumps(ScanConfig().model_dump(),indent=2))

@app.command("version")
def version_command():
    """Show installed version."""
    console.print(f"CORSCOPE {__version__}")

if __name__=="__main__": app()
