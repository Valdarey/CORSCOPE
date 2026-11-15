from corscope.modules.risk import assess_risks
def test_reflection_with_credentials_is_high():
    origins=[{"scenario":"external_origin","reflected":True,"allow_origin":"https://evil.test"}]
    credentials={"observations":[{"classification":"reflected_untrusted_origin_with_credentials"}]}
    result=assess_risks("https://x",origins,{},credentials,{})
    assert result[0]["severity"]=="High"
    assert result[0]["verified_vulnerability"] is False
def test_no_indicators_is_informational():
    result=assess_risks("https://x",[],{}, {"observations":[]},{})
    assert result[0]["severity"]=="Informational"
