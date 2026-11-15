"""Centralized, conservative HTTP client."""
import time
import logging
from dataclasses import dataclass
from typing import Mapping
import requests
from requests import Response
from corscope.config import ScanConfig

logger = logging.getLogger("corscope")

@dataclass
class HTTPResult:
    url: str
    method: str
    status_code: int | None
    headers: dict[str, str]
    elapsed_ms: float
    error: str | None = None

class HTTPClient:
    """Shared Requests session; sends no cookies or credentials by default."""
    def __init__(self, config: ScanConfig | None = None):
        self.config = config or ScanConfig()
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.config.user_agent})
        self.session.cookies.clear()

    def request(self, method: str, url: str, *, headers: Mapping[str, str] | None = None) -> HTTPResult:
        if self.config.delay:
            time.sleep(self.config.delay)
        started = time.perf_counter()
        try:
            response: Response = self.session.request(
                method, url, headers=dict(headers or {}), timeout=self.config.timeout,
                verify=self.config.verify_tls, allow_redirects=self.config.follow_redirects,
            )
            elapsed = (time.perf_counter() - started) * 1000
            # Do not persist response bodies: assessment relies on status and headers only.
            return HTTPResult(url, method.upper(), response.status_code,
                              {k: v for k, v in response.headers.items()}, elapsed)
        except requests.RequestException as exc:
            logger.warning("HTTP request failed (%s %s): %s", method, url, exc)
            return HTTPResult(url, method.upper(), None, {},
                              (time.perf_counter() - started) * 1000, str(exc))

    def close(self) -> None:
        self.session.close()
