"""Evidence-aware heuristic risk classification."""
def assess_risks(target: str, origins: list[dict], headers: dict, credentials: dict, preflight: dict) -> list[dict]:
    findings=[]
    reflected=[x for x in origins if x.get("scenario") in {"external_origin","untrusted_origin","different_subdomain","null_origin"} and x.get("reflected")]
    credentialed=[x for x in credentials["observations"] if x["classification"]=="reflected_untrusted_origin_with_credentials"]
    wildcard=any((x.get("allow_origin") or "").strip()=="*" for x in origins)
    if credentialed:
        findings.append({"severity":"High","title":"Untrusted Origin reflected with credentials enabled",
            "description":"A tested non-same-origin value was reflected while Access-Control-Allow-Credentials was true.",
            "evidence":credentialed,"risk_explanation":"If the origin is not trusted and the endpoint exposes sensitive authenticated data, browser-based cross-origin reads may be possible.",
            "recommendation":"Use an explicit allowlist of trusted origins; avoid reflecting arbitrary Origin values and enable credentials only where required.",
            "confidence":"Medium","verified_vulnerability":False})
    elif reflected:
        findings.append({"severity":"Medium","title":"Non-same-origin value reflected by CORS policy",
            "description":"One or more non-same-origin probes were reflected in Access-Control-Allow-Origin.",
            "evidence":reflected,"risk_explanation":"Reflection may indicate permissive origin validation; credential and endpoint context were not proven.",
            "recommendation":"Validate Origin against an exact trusted-origin allowlist and review all affected endpoints.",
            "confidence":"Medium","verified_vulnerability":False})
    if wildcard:
        findings.append({"severity":"Low","title":"Wildcard Access-Control-Allow-Origin observed",
            "description":"At least one probe received Access-Control-Allow-Origin: *.","evidence":[x for x in origins if x.get("allow_origin")=="*"],
            "risk_explanation":"Wildcard allows public cross-origin reads for non-credentialed requests; impact depends on response data.",
            "recommendation":"Use a specific origin policy when responses should not be publicly readable.","confidence":"High","verified_vulnerability":False})
    if not findings:
        findings.append({"severity":"Informational","title":"No high-confidence CORS misconfiguration indicator detected",
            "description":"The tested probes did not reveal reflected untrusted origins or wildcard ACAO.",
            "evidence":{"origin_probes":len(origins),"header_inspection":headers,"preflight":preflight},
            "risk_explanation":"This limited assessment cannot rule out endpoint-specific or authenticated CORS issues.",
            "recommendation":"Repeat assessment for relevant API endpoints and verify behavior in a browser when authorized.",
            "confidence":"Low","verified_vulnerability":False})
    return findings
