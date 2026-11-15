from corscope.modules.origin import analyze_origins
from corscope.core.http_client import HTTPResult
class FakeClient:
    def request(self, method, url, headers=None):
        origin=(headers or {}).get("Origin")
        return HTTPResult(url,method,200,{"Access-Control-Allow-Origin":origin or "https://site.test"},1.0)
def test_origin_probes_cover_scenarios():
    result=analyze_origins(FakeClient(),"https://site.test/path")
    assert [x["scenario"] for x in result]==["same_origin","external_origin","untrusted_origin","different_subdomain","null_origin"]
    assert all(x["reflected"] for x in result)
