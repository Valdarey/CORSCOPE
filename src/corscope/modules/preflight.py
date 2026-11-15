"""Perform a single conservative OPTIONS preflight probe."""
def analyze_preflight(client, target: str) -> dict:
    response=client.request("OPTIONS", target, headers={
        "Origin":"https://corscope-probe.invalid",
        "Access-Control-Request-Method":"PUT",
        "Access-Control-Request-Headers":"X-CORSCOPE-Test, Content-Type",
    })
    h={k.lower():v for k,v in response.headers.items()}
    methods=[x.strip().upper() for x in h.get("access-control-allow-methods", "").split(",") if x.strip()]
    allowed_headers=[x.strip() for x in h.get("access-control-allow-headers", "").split(",") if x.strip()]
    return {"status_code":response.status_code,"error":response.error,
            "allow_origin":h.get("access-control-allow-origin"),
            "allow_credentials":h.get("access-control-allow-credentials"),
            "allow_methods":methods,"allow_headers":allowed_headers,
            "put_listed": "PUT" in methods,"requested_custom_header_listed":
                any(x.lower()=="x-corscope-test" for x in allowed_headers),
            "notes":["A method listed in a preflight response is not proof that the browser can access a resource."]}
