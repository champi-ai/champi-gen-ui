#!/usr/bin/env bash
# Development environment setup script for champi-gen-ui

set -e  # Exit on error

echo "🚀 Setting up champi-gen-ui development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}UV not found. Installing UV...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo -e "${GREEN}✓ UV installed${NC}"
else
    echo -e "${GREEN}✓ UV is already installed${NC}"
fi

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(uv run python --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
REQUIRED_VERSION="3.12"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}✗ Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"

# Install dependencies
echo "Installing dependencies..."
uv sync --all-extras
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
uv run pre-commit install
uv run pre-commit install --hook-type commit-msg
echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"

# Create secrets baseline if it doesn't exist
if [ ! -f .secrets.baseline ]; then
    echo "Creating secrets baseline..."
    uv run detect-secrets scan > .secrets.baseline
    echo -e "${GREEN}✓ Secrets baseline created${NC}"
else
    echo -e "${GREEN}✓ Secrets baseline already exists${NC}"
fi

# Run initial checks
echo ""
echo "Running initial code quality checks..."

echo "  - Formatting check..."
if uv run ruff format --check . > /dev/null 2>&1; then
    echo -e "    ${GREEN}✓ Code is properly formatted${NC}"
else
    echo -e "    ${YELLOW}⚠ Some files need formatting (run: uv run ruff format .)${NC}"
fi

echo "  - Linting..."
if uv run ruff check . > /dev/null 2>&1; then
    echo -e "    ${GREEN}✓ No linting issues${NC}"
else
    echo -e "    ${YELLOW}⚠ Some linting issues found (run: uv run ruff check . --fix)${NC}"
fi

echo "  - Type checking..."
if uv run mypy src/ > /dev/null 2>&1; then
    echo -e "    ${GREEN}✓ Type checking passed${NC}"
else
    echo -e "    ${YELLOW}⚠ Type checking issues found (run: uv run mypy src/)${NC}"
fi

echo "  - Running tests..."
if uv run pytest --tb=short -q > /dev/null 2>&1; then
    echo -e "    ${GREEN}✓ All tests passed${NC}"
else
    echo -e "    ${YELLOW}⚠ Some tests failed (run: uv run pytest)${NC}"
fi

echo ""
echo -e "${GREEN}✨ Development environment setup complete!${NC}"
echo ""
echo "Quick commands:"
echo "  uv run pytest              # Run tests"
echo "  uv run ruff format .       # Format code"
echo "  uv run ruff check . --fix  # Fix linting issues"
echo "  uv run mypy src/           # Type check"
echo "  uv run cz commit           # Create a conventional commit"
echo "  uv run champi-gen-ui serve # Start the MCP server"
echo ""
echo "For more information, see CONTRIBUTING.md"
