"""Inspect CORS-related response headers."""
CORS_HEADERS = ["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials",
 "Access-Control-Allow-Methods", "Access-Control-Allow-Headers",
 "Access-Control-Expose-Headers", "Vary"]

def inspect_headers(response) -> dict:
    headers={k:v for k,v in response.headers.items() if k.lower() in {h.lower() for h in CORS_HEADERS}}
    normalized={k.lower():v for k,v in response.headers.items()}
    missing=[h for h in CORS_HEADERS[:-1] if h.lower() not in normalized]
    vary=normalized.get("vary", "")
    return {"status_code":response.status_code,"found":headers,"missing":missing,
            "vary_includes_origin": any(x.strip().lower()=="origin" for x in vary.split(",")),
            "notes":["Header presence alone does not establish exploitability."]}
