# Architecture

CORSCOPE uses a `src/` package layout and separates transport, assessment logic, presentation, and reporting.

## Workflow

1. CLI validates an absolute HTTP(S) URL.
2. `HTTPClient` sends a baseline GET, a compact set of Origin probes, and one OPTIONS preflight request.
3. Header, Origin, credential, and preflight analyzers normalize observations.
4. Risk Assessor correlates evidence and emits conservative findings.
5. Reporting adapters serialize the same assessment document to JSON, CSV, or HTML.

## Module responsibilities

- `core/`: URL validation, shared HTTP transport, orchestration.
- `modules/`: independent CORS analyzers and risk heuristics.
- `reporting/`: output serializers.
- `utils/`: shared helpers.

The response body is intentionally not stored. Modules share a single HTTP client configuration. No browser execution or credentialed request is performed.
