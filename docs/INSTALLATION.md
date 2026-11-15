# Installation

## Kali Linux

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv pipx git -y
pipx ensurepath
```

Restart the terminal if PATH changes, then from the project directory:

```bash
pipx install .
corscope --help
corscope --version
```

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest -v
ruff check .
```

