# Security and safe use

CORSCOPE is an assessment tool, not an exploitation framework. Only assess systems for which you have explicit authorization.

- URL syntax is validated, but targets are not allowlisted or restricted.
- TLS verification is enabled by default.
- Redirect following is disabled by default.
- Requests have a configurable timeout and optional delay.
- No cookies or authentication are intentionally supplied by CORSCOPE.
- No brute force, destructive methods, browser automation, or exploitation is performed.
- Response bodies are not retained; reports contain response headers and assessment evidence.

HTTP headers alone cannot prove browser exploitability or sensitive data exposure. Browser CORS enforcement, preflight caching, proxies, redirects, endpoint-specific behavior, and authentication state may affect results. Treat findings as configuration indicators requiring authorized validation.
