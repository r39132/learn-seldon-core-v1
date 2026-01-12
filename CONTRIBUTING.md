# Contributing to Sentiment Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Run setup: `./scripts/setup.sh`
4. Create a branch: `git checkout -b feature/your-feature`

## Development Workflow

### Code Quality

Before submitting a PR, ensure:

```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test-cov

# Run pre-commit hooks
make pre-commit
```

### Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

Example: `feat: add support for multi-language sentiment analysis`

### Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update README.md with details of changes
5. Request review from maintainers

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all functions/classes
- Keep functions small and focused
- Maximum line length: 100 characters

## Testing

- Write unit tests for new features
- Maintain test coverage above 80%
- Test edge cases
- Use fixtures for common test data

## Questions?

Open an issue for discussion or questions.

Thank you for contributing! 🎉
