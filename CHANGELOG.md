# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-10-03

### Added
- Initial project setup with comprehensive development infrastructure
- MCP server for generative UI through ImGui and Python
- Core canvas management system with 5 modes (standard, docking, multi-viewport, fullscreen, overlay)
- Widget system with 150+ widget types from ImGui core and extensions
- 200+ MCP tools for comprehensive UI creation across 20 categories
- Animation system with keyframe support and multiple easing functions
- Data binding for reactive UI updates
- JSON serialization for saving/loading UI definitions
- Code generation to export standalone Python scripts
- Template system for reusable UI patterns
- Integration with 10+ powerful extensions (ImPlot, ImNodes, file dialogs, etc.)
- Comprehensive documentation in `/docs` directory
- Development tooling setup:
  - Ruff for linting and formatting
  - MyPy for type checking
  - Pytest with coverage reporting
  - Pre-commit hooks for code quality
  - Commitizen for conventional commits
  - Detect-secrets for security scanning
- GitHub Actions CI/CD workflows:
  - Automated testing across Python 3.12 and 3.13
  - Security scanning with Bandit and detect-secrets
  - Package building and validation
  - Automated release workflow with semantic versioning
  - Pre-commit hook auto-updates
  - Dependency review for PRs
- MIT License
- Comprehensive `.gitignore` for Python projects
- Example usage demonstrations

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- Added secrets detection with detect-secrets
- Security scanning with Bandit in CI/CD pipeline
- Comprehensive `.gitignore` to prevent credential leakage

[Unreleased]: https://github.com/divagnz/champi-gen-ui/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/divagnz/champi-gen-ui/releases/tag/v0.1.0
