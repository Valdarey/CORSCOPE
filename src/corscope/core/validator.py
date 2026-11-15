"""URL validation without target allowlisting."""
from urllib.parse import urlsplit

class InvalidTargetError(ValueError):
    """Raised when a target is not a valid HTTP(S) URL."""

def validate_target(target: str) -> str:
    """Validate and normalize an absolute HTTP or HTTPS URL."""
    if not isinstance(target, str) or not target.strip():
        raise InvalidTargetError("Target URL is required.")
    value = target.strip()
    try:
        parsed = urlsplit(value)
        # Accessing port forces urllib to validate malformed port values.
        _ = parsed.port
    except ValueError as exc:
        raise InvalidTargetError(f"Malformed target URL: {exc}") from exc
    if parsed.scheme.lower() not in {"http", "https"}:
        raise InvalidTargetError("Only http:// and https:// targets are supported.")
    if not parsed.hostname:
        raise InvalidTargetError("Target URL must include a valid hostname.")
    if any(ch.isspace() for ch in value):
        raise InvalidTargetError("Target URL must not contain whitespace.")
    return value
