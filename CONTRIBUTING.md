# Contributing to Marketing Analyst Agent

Thank you for considering contributing to the Marketing Analyst Agent! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports:

- Check the issue tracker to see if the bug has already been reported
- Gather information to help reproduce and describe the bug

When reporting bugs:

1. Use the bug report template if available
2. Provide a clear title and description
3. Include steps to reproduce the bug
4. Describe expected vs. actual behavior
5. Include environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! When suggesting enhancements:

1. Use the feature request template if available
2. Provide a clear title and description
3. Explain why this enhancement would be useful
4. Suggest an implementation approach if possible

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature/bugfix
3. Make your changes
4. Ensure tests pass and add new tests if appropriate
5. Update documentation to reflect your changes
6. Submit a pull request

## Development Workflow

### Setting Up Development Environment

1. Clone the repository

   ```bash
   git clone https://github.com/yourusername/market_analyst_agent.git
   cd market_analyst_agent
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Install development dependencies
   ```bash
   pip install pytest black mypy
   ```

### Testing

Run tests with pytest:

```bash
pytest
```

### Code Style

This project follows PEP 8 style guidelines. Please use Black to format your code:

```bash
black .
```

### Documentation

- Update the README.md if you change functionality
- Add/update docstrings for new/modified functions and classes
- If you add a new feature, consider adding documentation to the docs/ folder

## Project Structure

```
market_analyst_agent/
├── docs/                    # Documentation files
├── src/                     # Source code
│   ├── agents/              # Agent definitions
│   ├── tools/               # Custom tools
│   ├── config/              # Configuration
│   └── utils/               # Utility functions
├── tests/                   # Test files
├── .env                     # Environment variables (not versioned)
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

## Documentation Guidelines

When adding new documentation:

1. Place feature documentation in the docs/ folder
2. Each feature requires a markdown file with:
   - Detailed description
   - Purpose statement
   - Mermaid diagram using theme colors (dark gray and light purple)
3. Use consistent naming convention: feature_name.md
4. Keep documentation up-to-date with code changes
5. Include usage examples where appropriate

## Adding New Tools

When adding new tools to the agent:

1. Create a new file in the `src/tools/` directory
2. Use the existing tool structure as a template
3. Define a Pydantic model for the tool inputs
4. Implement the tool's `_run` method
5. Add the new tool to the agent's tools list in `src/agents/marketing_analyst.py`
6. Add tests for the new tool
7. Document the new tool in the docs/ folder

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT license.
