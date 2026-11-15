import pytest
from corscope.core.validator import validate_target, InvalidTargetError
@pytest.mark.parametrize("url",["https://example.com","http://localhost:8000/path"])
def test_valid_urls(url): assert validate_target(url)==url
def test_invalid_scheme():
    with pytest.raises(InvalidTargetError): validate_target("ftp://example.com")
def test_malformed_port():
    with pytest.raises(InvalidTargetError): validate_target("https://example.com:bad")
