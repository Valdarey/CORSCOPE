"""Probe CORS behavior using a small set of non-destructive Origin values."""
from urllib.parse import urlsplit
from corscope.core.http_client import HTTPClient

def _origin_of(url: str) -> str:
    p = urlsplit(url); return f"{p.scheme}://{p.netloc}"

def analyze_origins(client: HTTPClient, target: str) -> list[dict]:
    base = _origin_of(target)
    probes = [
        ("same_origin", base),
        ("external_origin", "https://corscope-probe.invalid"),
        ("untrusted_origin", "https://untrusted-corscope.invalid"),
        ("different_subdomain", f"https://corscope.{urlsplit(target).hostname}"),
        ("null_origin", "null"),
    ]
    results=[]
    for name, origin in probes:
        result=client.request("GET", target, headers={"Origin": origin})
        allow_origin=result.headers.get("Access-Control-Allow-Origin") or result.headers.get("access-control-allow-origin")
        allow_credentials=result.headers.get("Access-Control-Allow-Credentials") or result.headers.get("access-control-allow-credentials")
        results.append({"scenario":name,"sent_origin":origin,"status_code":result.status_code,
                        "allow_origin":allow_origin,"allow_credentials":allow_credentials,
                        "reflected": allow_origin == origin,
                        "error":result.error,"response_headers":result.headers})
    return results
