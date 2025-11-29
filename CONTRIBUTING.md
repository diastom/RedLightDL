# Contributing to RedLight DL

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/diastom/RedLightDL/issues)
2. If not, create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)

### Suggesting Features

Open an issue with:
- Clear description of the feature
- Use cases
- Why it would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/diastom/RedLightDL.git
cd RedLightDL

# Install in development mode
pip install -e .

# Install dev dependencies
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

## Testing

Before submitting a PR, test your changes:

```bash
# Test installation
pip install -e .

# Test CLI
ph-shorts --help

# Test download
ph-shorts "TEST_URL"
```

## Questions?

Feel free to open an issue for any questions!
