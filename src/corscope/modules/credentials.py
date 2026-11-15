"""Analyze credential and origin combinations without claiming exploitation."""
def analyze_credentials(origin_results: list[dict]) -> dict:
    observations=[]
    for item in origin_results:
        allow=(item.get("allow_origin") or "").strip()
        creds=(item.get("allow_credentials") or "").strip().lower()=="true"
        if allow == "*" and creds:
            classification="wildcard_with_credentials_invalid_for_browser_credentialed_read"
            note="Wildcard ACAO cannot be used by browsers for credentialed CORS response reads."
        elif item.get("reflected") and creds and item.get("scenario") not in {"same_origin"}:
            classification="reflected_untrusted_origin_with_credentials"
            note="Potentially risky combination; trust policy and browser behavior require validation."
        elif creds:
            classification="credentials_enabled"
            note="Credentials are enabled; assess the allowed-origin policy and endpoint context."
        else:
            classification="no_credentialed_cors_indicator"
            note="No true credential allowance observed for this probe."
        observations.append({"scenario":item.get("scenario"),"allow_origin":allow,
                             "allow_credentials":creds,"classification":classification,"note":note,
                             "status_code":item.get("status_code")})
    return {"observations":observations,"sensitive_data_access_verified":False,
            "summary":"Configuration indicators only; no authenticated data access was attempted."}
