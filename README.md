# CORSCOPE

**Modular CORS Security Assessment CLI Tool** — version 1.0.0

CORSCOPE is a Python CLI for assessing Cross-Origin Resource Sharing (CORS) response configuration. It checks HTTP response headers, probes a small set of Origin values, analyzes credential-related configuration, inspects an OPTIONS preflight response, classifies evidence, and generates JSON, CSV, or HTML reports.

> Use only against systems you own or are explicitly authorized to test. CORSCOPE is an assessment tool, not an exploitation framework. Header-based results do not prove browser exploitability or sensitive-data exposure.

## Features

- Modular Origin Analyzer, Header Inspector, Credential Analyzer, Preflight Analyzer, and Risk Assessor.
- Shared Requests session, URL validation, configurable timeout/delay, TLS verification enabled by default, redirects disabled by default.
- No cookies or authentication supplied by default; response bodies are not stored.
- JSON, CSV, and HTML reporting.
- Pytest suite, Ruff linting, and GitHub Actions for Python 3.10–3.12.

## Installation (Kali Linux)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv pipx git -y
pipx ensurepath
# From the cloned repository:
pipx install .
corscope --help
corscope --version
```

## Usage

```bash
corscope scan https://lab.example
corscope scan https://lab.example --output json
corscope scan https://lab.example --output html --report assessment.html
corscope scan https://lab.example --output csv --delay 0.5 --timeout 15
corscope origin https://lab.example
corscope headers https://lab.example
corscope preflight https://lab.example
corscope report corscope-report.json --output html
corscope config
corscope --help
```

Output formats default to `corscope-report.json`, `.csv`, or `.html` when `--report` is omitted. Individual analyzer commands currently run the common assessment pipeline and retain the selected module's data in the report.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest -v
ruff check .
```

## Assessment notes

The default scan sends one baseline GET, five GET requests with different Origin values, and one OPTIONS preflight request. All probes are non-destructive. `--no-verify-tls` exists for controlled lab use only. Redirects remain disabled unless explicitly enabled. Findings are heuristic and include confidence, evidence, and recommendations. In particular, `Access-Control-Allow-Origin: *` combined with credentials is not treated as a successful credentialed browser read.

## Project layout

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/INSTALLATION.md](docs/INSTALLATION.md), and [docs/SECURITY.md](docs/SECURITY.md).

## Roadmap

- **v1.0:** CLI, core assessment, reports, tests, CI, documentation.
- **v1.5:** richer origin validation, SQLite, profiles, improved evidence.
- **v2.0:** plugin modules, browser-based verification, CI/CD integration.

## License

MIT. See [LICENSE](LICENSE).
