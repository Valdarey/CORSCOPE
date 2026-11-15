"""Assessment orchestration."""
from datetime import datetime, timezone
from corscope import __version__
from corscope.core.http_client import HTTPClient
from corscope.modules.headers import inspect_headers
from corscope.modules.origin import analyze_origins
from corscope.modules.credentials import analyze_credentials
from corscope.modules.preflight import analyze_preflight
from corscope.modules.risk import assess_risks

class AssessmentEngine:
    def __init__(self, client: HTTPClient): self.client = client
    def scan(self, target: str) -> dict:
        baseline = self.client.request("GET", target)
        origin_results = analyze_origins(self.client, target)
        preflight = analyze_preflight(self.client, target)
        header_result = inspect_headers(baseline)
        credential = analyze_credentials(origin_results)
        findings = assess_risks(target, origin_results, header_result, credential, preflight)
        return {
            "target": target, "timestamp": datetime.now(timezone.utc).isoformat(),
            "corscope_version": __version__,
            "http": {"status_code": baseline.status_code, "headers": baseline.headers,
                     "elapsed_ms": round(baseline.elapsed_ms, 2), "error": baseline.error},
            "origin_analysis": origin_results, "header_inspection": header_result,
            "credential_analysis": credential, "preflight_analysis": preflight,
            "findings": findings,
            "limitations": ["Assessment is based on HTTP status and response headers only.",
                "No browser-based CORS enforcement or sensitive-data access was verified.",
                "Endpoint-specific behavior, proxies, redirects and authentication state may differ."],
        }
