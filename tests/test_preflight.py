from corscope.modules.preflight import analyze_preflight
from corscope.core.http_client import HTTPResult
class Fake:
    def request(self,method,url,headers=None):
        assert method=="OPTIONS"
        return HTTPResult(url,method,204,{"Access-Control-Allow-Methods":"GET, PUT","Access-Control-Allow-Headers":"X-CORSCOPE-Test, Content-Type"},2)
def test_preflight_parsing():
    result=analyze_preflight(Fake(),"https://x.test")
    assert result["put_listed"] is True
    assert result["requested_custom_header_listed"] is True
