# Contributing to Champi-Gen-UI

Thank you for your interest in contributing to Champi-Gen-UI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Development Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/yourusername/champi-gen-ui.git
   cd champi-gen-ui
   ```

2. **Install UV (if not already installed):**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies:**

   ```bash
   uv sync --all-extras
   ```

4. **Install pre-commit hooks:**

   ```bash
   uv run pre-commit install
   uv run pre-commit install --hook-type commit-msg
   ```

5. **Verify the setup:**

   ```bash
   uv run pytest
   uv run ruff check .
   uv run mypy src/
   ```

## Development Workflow

### Branch Naming

Use descriptive branch names with prefixes:

- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications
- `chore/` - Maintenance tasks

Example: `feat/add-new-widget`, `fix/canvas-rendering-issue`

### Making Changes

1. Create a new branch:

   ```bash
   git checkout -b feat/your-feature-name
   ```

2. Make your changes following our coding standards

3. Run tests and linters:

   ```bash
   uv run pytest
   uv run ruff check . --fix
   uv run ruff format .
   uv run mypy src/
   ```

4. Commit your changes using conventional commits (see below)

5. Push to your fork and create a pull request

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Maximum line length: 88 characters (Black/Ruff default)
- Use double quotes for strings
- Import order: standard library, third-party, local (managed by Ruff)

### Code Quality Tools

We use the following tools to maintain code quality:

- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Bandit**: Security vulnerability scanning
- **Pytest**: Testing framework with coverage

### Pre-commit Hooks

All code is automatically checked by pre-commit hooks before committing:

- Code formatting (Ruff)
- Linting (Ruff, Bandit)
- Type checking (MyPy)
- Secrets detection (detect-secrets)
- YAML/JSON/TOML validation
- Trailing whitespace removal
- Conventional commit message validation

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/) for all commit messages.

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system or dependency changes
- `ci`: CI/CD configuration changes
- `chore`: Other changes that don't modify src or test files

### Examples

```bash
# Good commit messages
feat: add support for custom widget themes
fix: resolve canvas rendering issue in docking mode
docs: update installation instructions in README
refactor: simplify widget registry implementation
test: add unit tests for animation system

# With scope
feat(widgets): add new slider widget with custom styling
fix(canvas): correct viewport calculation in multi-monitor setup

# With body and footer
feat: implement keyframe animation system

Add support for keyframe-based animations with multiple easing functions.
Includes timeline controls and animation preview.

Closes #123
```

### Using Commitizen

We recommend using Commitizen for creating commits:

```bash
uv run cz commit
```

This will guide you through creating a properly formatted commit message.

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=champi_gen_ui --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_widgets.py

# Run tests with specific marker
uv run pytest -m "not slow"
```

### Test Markers

- `slow`: Tests that take longer to run
- `integration`: Integration tests
- `visual`: Tests requiring visual verification

### Writing Tests

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names: `test_widget_renders_correctly_with_default_props`
- Include docstrings explaining what the test validates
- Aim for >80% code coverage

## Pull Request Process

1. **Update documentation** if you've made changes to the API or added new features

2. **Ensure all checks pass:**
   - All tests passing
   - Code coverage maintained or improved
   - No linting errors
   - Type checking passes
   - Security scans clean

3. **Update CHANGELOG.md** with your changes (the release process will handle versioning)

4. **Create a pull request:**
   - Use a descriptive title following conventional commit format
   - Provide a clear description of the changes
   - Reference any related issues
   - Add screenshots for UI changes

5. **Address review feedback:**
   - Respond to all comments
   - Make requested changes
   - Keep the PR focused on a single feature/fix

6. **Squash commits** if requested before merging

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No new warnings or errors
```

## Release Process

Releases are managed automatically using semantic versioning and GitHub Actions.

### Version Bumping

The project uses Commitizen for automatic versioning based on conventional commits:

- `feat:` commits trigger a minor version bump (0.1.0 → 0.2.0)
- `fix:` commits trigger a patch version bump (0.1.0 → 0.1.1)
- `BREAKING CHANGE:` in commit body triggers a major version bump (0.1.0 → 1.0.0)

### Creating a Release

Releases are created via GitHub Actions workflow:

1. Go to Actions → Release workflow
2. Click "Run workflow"
3. Select version bump type (major/minor/patch)
4. The workflow will:
   - Bump version in all relevant files
   - Update CHANGELOG.md
   - Create a git tag
   - Build the package
   - Create a GitHub release
   - Publish to PyPI (if on main branch)

### Manual Version Bump

If you need to bump the version manually:

```bash
# Patch version (0.1.0 → 0.1.1)
uv run cz bump --increment PATCH

# Minor version (0.1.0 → 0.2.0)
uv run cz bump --increment MINOR

# Major version (0.1.0 → 1.0.0)
uv run cz bump --increment MAJOR
```

## Questions or Issues?

- Check existing [issues](https://github.com/divagnz/champi-gen-ui/issues)
- Create a new issue for bugs or feature requests
- Join our [discussions](https://github.com/divagnz/champi-gen-ui/discussions) for questions

## License

By contributing to Champi-Gen-UI, you agree that your contributions will be licensed under the MIT License.
