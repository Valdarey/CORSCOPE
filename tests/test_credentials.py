from corscope.modules.credentials import analyze_credentials
def test_wildcard_credentials_not_called_exploitable():
    result=analyze_credentials([{"scenario":"external_origin","allow_origin":"*","allow_credentials":"true","status_code":200}])
    assert result["observations"][0]["classification"].startswith("wildcard_")
    assert result["sensitive_data_access_verified"] is False
def test_reflection_with_credentials_flagged():
    result=analyze_credentials([{"scenario":"external_origin","allow_origin":"https://x","allow_credentials":"true","reflected":True,"status_code":200}])
    assert result["observations"][0]["classification"]=="reflected_untrusted_origin_with_credentials"
