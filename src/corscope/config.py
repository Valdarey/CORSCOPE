"""Application defaults and configuration models."""
from pydantic import BaseModel, Field

class ScanConfig(BaseModel):
    timeout: float = Field(default=10.0, gt=0, le=120)
    delay: float = Field(default=0.0, ge=0, le=60)
    verify_tls: bool = True
    follow_redirects: bool = False
    user_agent: str = "CORSCOPE/1.0.0 (authorized security assessment)"
