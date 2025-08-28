# Real Estate Scraper Bot

## Development

### Code Formatting

```bash
ruff format --config pyproject.toml ./
```

### Code Checking

```bash
ruff check --config pyproject.toml ./ --fix
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pip install -r requirements.txt
pre-commit install
```

Run hooks manually:

```bash
pre-commit run --all-files
```
