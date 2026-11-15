from corscope.modules.headers import inspect_headers
from corscope.core.http_client import HTTPResult
def test_header_inspection():
    r=HTTPResult("https://x", "GET",200,{"Access-Control-Allow-Origin":"*","Vary":"Accept-Encoding, Origin"},1)
    result=inspect_headers(r)
    assert result["found"]["Access-Control-Allow-Origin"]=="*"
    assert result["vary_includes_origin"] is True
    assert "Access-Control-Allow-Credentials" in result["missing"]
