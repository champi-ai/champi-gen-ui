# Repository Setup Summary

## Overview

The champi-gen-ui repository has been configured with comprehensive development infrastructure following modern Python best practices. This document summarizes all configurations and provides quick reference for developers.

## Repository Information

- **Project Name**: champi-gen-ui
- **Description**: MCP server for generative UI through ImGui and Python
- **Python Version**: 3.12+
- **Package Manager**: UV
- **License**: MIT
- **Current Version**: 0.1.0

## Infrastructure Components

### 1. Package Management & Dependencies

**Configuration File**: `pyproject.toml`

- **Build System**: Hatchling
- **Package Manager**: UV with managed dependencies
- **Core Dependencies**:
  - fastmcp >= 2.12.0 (MCP server framework)
  - imgui-bundle >= 1.5.0 (ImGui Python bindings)
  - pyglm >= 2.7.0 (OpenGL Mathematics)
  - loguru >= 0.7.0 (Logging)
  - pydantic >= 2.0.0 (Data validation)

- **Development Dependencies**:
  - pytest >= 8.0.0 (Testing framework)
  - pytest-asyncio >= 0.23.0 (Async test support)
  - pytest-cov >= 4.1.0 (Coverage reporting)
  - ruff >= 0.8.0 (Linting & formatting)
  - mypy >= 1.8.0 (Type checking)
  - pre-commit >= 3.0.0 (Git hooks)
  - commitizen >= 3.0.0 (Conventional commits)
  - detect-secrets >= 1.4.0 (Secrets detection)

### 2. Code Quality & Linting

**Ruff Configuration** (in pyproject.toml):
- Target version: Python 3.12
- Line length: 88 characters
- Enabled rules: pycodestyle, Pyflakes, pyupgrade, flake8-bugbear, flake8-simplify, isort, pep8-naming, mccabe
- Auto-fix enabled for all fixable issues
- Import sorting with first-party package detection

**MyPy Configuration** (in pyproject.toml):
- Python version: 3.12
- Type checking for untyped definitions
- Strict equality checks
- Redundant cast warnings
- Unused ignore warnings
- Ignored modules: imgui_bundle, pyglm (missing type stubs)

**Bandit Configuration** (in pyproject.toml):
- Security linting for source code
- Excludes: tests, examples, virtual environments
- Skip B101 (assert in tests), B601 (paramiko)

### 3. Pre-commit Hooks

**Configuration File**: `.pre-commit-config.yaml`

**Hooks Configured**:

1. **General Pre-commit Hooks**:
   - Trailing whitespace removal
   - End-of-file fixing
   - YAML/JSON/TOML validation
   - Large file detection (max 1MB)
   - Merge conflict detection
   - Case conflict detection
   - Private key detection
   - Mixed line-ending normalization (LF)

2. **Python Quality Hooks**:
   - Ruff formatter (code formatting)
   - Ruff linter (with auto-fix)
   - MyPy type checking (excludes tests/examples)
   - Bandit security scanning
   - Pydocstyle (Google convention, relaxed for tests)

3. **Security Hooks**:
   - detect-secrets (with baseline file)
   - Bandit security vulnerability scanning

4. **Commit Message Hooks**:
   - Conventional commits enforcement

5. **Additional Hooks**:
   - Markdown linting (with auto-fix)
   - YAML formatting (2-space indent)

**Installation Commands**:
```bash
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

### 4. Conventional Commits & Versioning

**Commitizen Configuration** (in pyproject.toml):

- **Commit Style**: Conventional Commits
- **Version Format**: v{version}
- **Version Files**:
  - pyproject.toml:version
  - src/champi_gen_ui/__init__.py:__version__
- **Changelog**: Automatic generation in CHANGELOG.md
- **Commit Message Format**: `bump: version $current_version → $new_version`

**Commit Types**:
- `feat`: New feature (minor version bump)
- `fix`: Bug fix (patch version bump)
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/updates
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks
- `BREAKING CHANGE`: Major version bump

**Usage**:
```bash
uv run cz commit  # Interactive commit creation
uv run cz bump    # Auto version bump based on commits
```

### 5. Security & Secrets Protection

**Configuration Files**: `.gitignore`, `.secrets.baseline`

**Git Ignore Patterns**:
- Python artifacts (__pycache__, *.pyc, *.pyo, etc.)
- Virtual environments (.venv, venv, env)
- IDE files (.vscode, .idea, *.swp)
- OS files (.DS_Store, Thumbs.db)
- Build artifacts (dist, build, *.egg-info)
- Test coverage (.coverage, htmlcov)
- Environment files (.env, .env.*)
- Secrets baseline (.secrets.baseline)
- UV cache (.uv_cache)
- Jupyter notebooks (.ipynb_checkpoints)

**Secrets Detection**:
- Baseline file: `.secrets.baseline`
- Pre-commit hook scans for secrets
- CI/CD pipeline includes secrets scanning
- Detects: API keys, tokens, passwords, private keys

### 6. CI/CD Workflows

**Location**: `.github/workflows/`

#### 6.1 CI Workflow (`ci.yml`)

**Triggers**: Push/PR to main, develop branches

**Jobs**:

1. **Lint and Test**:
   - Matrix testing: Python 3.12, 3.13
   - Ruff format checking
   - Ruff linting
   - MyPy type checking
   - Pytest with coverage
   - Codecov upload

2. **Security Checks**:
   - Bandit security scanning
   - detect-secrets scanning
   - Security report artifacts

3. **Build Package**:
   - UV build
   - Package metadata validation with twine
   - Build artifacts upload

#### 6.2 Release Workflow (`release.yml`)

**Trigger**: Manual workflow dispatch

**Features**:
- Version bump selection (major/minor/patch)
- Automatic changelog update
- Git tag creation
- GitHub release creation
- PyPI publishing (main branch only)

**Usage**: GitHub Actions → Release → Run workflow → Select bump type

#### 6.3 Pre-commit Auto-update (`pre-commit-autoupdate.yml`)

**Trigger**: Weekly (Monday midnight) or manual

**Features**:
- Automatic pre-commit hook updates
- Creates PR with updates
- Labels: dependencies, automation

#### 6.4 Dependency Review (`dependency-review.yml`)

**Trigger**: Pull requests to main, develop

**Features**:
- Reviews dependency changes
- Fails on moderate+ severity vulnerabilities
- Denies AGPL-3.0, GPL-3.0 licenses
- Comments on PR with findings

### 7. Testing Infrastructure

**Pytest Configuration** (in pyproject.toml):

- **Test Directory**: tests/
- **Test Pattern**: test_*.py
- **Coverage**: champi_gen_ui package
- **Reports**: Terminal (missing lines), HTML
- **Async Support**: Auto mode
- **Markers**:
  - `slow`: Long-running tests
  - `integration`: Integration tests
  - `visual`: Visual verification tests

**Coverage Configuration**:
- **Source**: src/
- **Branch Coverage**: Enabled
- **Omit**: tests/, examples/
- **Precision**: 2 decimal places
- **Exclude Lines**: pragma: no cover, __repr__, if __name__, raise assertions

**Commands**:
```bash
uv run pytest                    # Run all tests
uv run pytest --cov              # With coverage
uv run pytest -m "not slow"      # Skip slow tests
uv run pytest --cov-report=html  # HTML coverage report
```

### 8. Documentation

**Files Created**:

1. **CHANGELOG.md**: Version history with semantic versioning
2. **CONTRIBUTING.md**: Comprehensive contribution guidelines
3. **LICENSE**: MIT License (2025 Divagnz)
4. **README.md**: Already existing, comprehensive project documentation
5. **SETUP_SUMMARY.md**: This file - infrastructure overview

### 9. Development Tools

**Setup Script**: `setup-dev.sh`

**Features**:
- UV installation check
- Python version verification
- Dependency installation
- Pre-commit hooks setup
- Secrets baseline creation
- Initial quality checks (format, lint, type, test)

**Usage**:
```bash
./setup-dev.sh
```

**Environment Configuration**: `.env.example`
- Debug settings
- Log level configuration
- ImGui settings
- MCP server configuration

## Quick Start for New Developers

### 1. Initial Setup

```bash
# Clone repository
git clone https://github.com/divagnz/champi-gen-ui.git
cd champi-gen-ui

# Run setup script
./setup-dev.sh

# Or manual setup:
uv sync --all-extras
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
```

### 2. Development Workflow

```bash
# Create feature branch
git checkout -b feat/my-feature

# Make changes, then check quality
uv run ruff format .           # Format code
uv run ruff check . --fix      # Fix linting issues
uv run mypy src/               # Type check
uv run pytest                  # Run tests

# Commit with conventional commits
uv run cz commit

# Push and create PR
git push -u origin feat/my-feature
```

### 3. Common Commands

```bash
# Development
uv run champi-gen-ui serve     # Start MCP server
uv run pytest --cov            # Test with coverage
uv run ruff check . --fix      # Auto-fix linting

# Version Management
uv run cz bump                 # Auto version bump
uv run cz changelog            # Generate changelog

# Pre-commit
uv run pre-commit run --all-files  # Run all hooks
uv run pre-commit autoupdate       # Update hook versions
```

## File Structure

```
champi-gen-ui/
├── .github/
│   └── workflows/
│       ├── ci.yml                      # Main CI pipeline
│       ├── release.yml                 # Release automation
│       ├── dependency-review.yml       # Dependency scanning
│       └── pre-commit-autoupdate.yml   # Hook updates
├── src/champi_gen_ui/              # Source code
├── tests/                          # Test suite
├── docs/                           # Documentation
├── examples/                       # Usage examples
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore patterns
├── .pre-commit-config.yaml         # Pre-commit hooks
├── .python-version                 # Python version (3.12)
├── .secrets.baseline               # Secrets detection baseline
├── CHANGELOG.md                    # Version history
├── CONTRIBUTING.md                 # Contribution guide
├── LICENSE                         # MIT License
├── README.md                       # Project documentation
├── SETUP_SUMMARY.md                # This file
├── pyproject.toml                  # Project configuration
├── setup-dev.sh                    # Development setup script
└── uv.lock                         # Dependency lock file
```

## Configuration Files Reference

| File | Purpose | Key Settings |
|------|---------|-------------|
| `pyproject.toml` | Project metadata, dependencies, tool configs | Build system, dependencies, ruff, mypy, pytest, coverage, commitizen, bandit |
| `.pre-commit-config.yaml` | Git hook configurations | Pre-commit hooks for formatting, linting, security, commit messages |
| `.gitignore` | Git exclusions | Python artifacts, IDE files, secrets, build outputs |
| `.github/workflows/*.yml` | CI/CD pipelines | Testing, security, releases, dependency reviews |
| `setup-dev.sh` | Development setup automation | Environment validation and initialization |
| `.env.example` | Environment variables template | Application and development settings |

## Best Practices Enforced

1. **Code Quality**:
   - PEP 8 compliance via Ruff
   - Type hints via MyPy
   - 88 character line limit
   - Import sorting
   - Docstring standards (Google style)

2. **Security**:
   - Secrets detection
   - Security vulnerability scanning (Bandit)
   - Dependency review in PRs
   - License compliance checks

3. **Version Control**:
   - Conventional commits enforced
   - Semantic versioning automated
   - Automatic changelog generation
   - Protected branches (via CI)

4. **Testing**:
   - >80% code coverage target
   - Unit and integration test separation
   - Async test support
   - Multiple Python version testing

5. **Documentation**:
   - Comprehensive README
   - API documentation
   - Contributing guidelines
   - Changelog maintenance

## Maintenance Tasks

### Weekly (Automated)
- Pre-commit hook updates (via GitHub Actions)

### Per Commit
- Pre-commit hooks run automatically
- Code formatting and linting
- Secrets scanning
- Commit message validation

### Per PR
- CI pipeline runs (test, lint, security)
- Dependency review
- Coverage reporting

### Per Release
- Version bump
- Changelog update
- GitHub release creation
- PyPI publishing

## Troubleshooting

### Pre-commit Hook Issues

```bash
# Reinstall hooks
uv run pre-commit uninstall
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg

# Clear cache and retry
uv run pre-commit clean
uv run pre-commit run --all-files
```

### Dependency Issues

```bash
# Re-sync dependencies
uv sync --all-extras

# Clear cache
rm -rf .venv uv.lock
uv sync --all-extras
```

### Type Checking Failures

```bash
# Install type stubs
uv pip install types-setuptools

# Skip mypy temporarily (not recommended)
SKIP=mypy git commit -m "feat: your message"
```

## Additional Resources

- **Project Repository**: https://github.com/divagnz/champi-gen-ui
- **Issue Tracker**: https://github.com/divagnz/champi-gen-ui/issues
- **Discussions**: https://github.com/divagnz/champi-gen-ui/discussions
- **UV Documentation**: https://github.com/astral-sh/uv
- **Ruff Documentation**: https://docs.astral.sh/ruff/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Commitizen**: https://commitizen-tools.github.io/commitizen/

---

**Last Updated**: 2025-10-03
**Setup Version**: 1.0.0
