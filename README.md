# Marketing Analyst Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)

An AI-powered marketing analyst agent built with Langchain that automates marketing analysis tasks through a command-line interface.

## Overview

This project implements an intelligent agent system capable of analyzing marketing data, generating insights, and providing strategic recommendations - effectively replacing or augmenting human marketing analysts with AI capabilities.

## Features

- Market trend analysis and forecasting
- Consumer sentiment analysis
- Campaign performance evaluation
- Competitor analysis
- Automated report generation
- Strategy recommendations
- Data visualization capabilities

## Prerequisites

- Python 3.9+
- OpenAI API key (optional when using DEBUG_MODE)
- LangSmith account for tracing and evaluation (optional)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/market_analyst_agent.git
cd market_analyst_agent
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
LANGSMITH_API_KEY=your_langsmith_api_key  # Optional, for tracing
LANGSMITH_PROJECT=your_langsmith_project_name  # Optional, for tracing
DEBUG_MODE=true  # Set to true for development without API keys
```

## Project Structure

```
market_analyst_agent/
├── docs/                    # Documentation files
├── src/                     # Source code
│   ├── agents/              # Agent definitions
│   ├── chains/              # LangChain chains
│   ├── tools/               # Custom tools
│   ├── models/              # Data models
│   ├── config/              # Configuration
│   └── utils/               # Utility functions
├── tests/                   # Test files
├── .env                     # Environment variables (not versioned)
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

## Usage

### Running the agent:

For a single query:

```bash
python -m src.main --query "Analyze market trends in the mobile gaming industry"
```

With specific model:

```bash
python -m src.main --model gpt-4 --query "What is the consumer sentiment around Product X?"
```

With term highlighting:

```bash
python -m src.main --query "Analyze mobile gaming market trends" --highlight "growth" "revenue" "engagement"
```

In interactive mode:

```bash
python -m src.main
```

### Using the Convenience Script

A shell script is provided for easier usage with automatic virtual environment management:

```bash
# Basic usage (interactive mode)
./run_agent.sh

# Query with highlighting
./run_agent.sh -q "Analyze mobile gaming market trends" -h growth revenue engagement

# Full options
./run_agent.sh -q "Your query here" -m gpt-4 -v -h term1 term2
```

Available options:

- `-q, --query`: The query to process
- `-m, --model`: OpenAI model to use
- `-v, --verbose`: Enable verbose output
- `-n, --no-tracing`: Disable LangSmith tracing
- `-h, --highlight`: Terms to highlight (multiple can be specified)
- `-i, --interactive`: Force interactive mode

### Command-line Arguments

- `--query`: The query to run (if not provided, interactive mode will be used)
- `--model`: OpenAI model to use (default: specified in .env)
- `--no-tracing`: Disable LangSmith tracing
- `--verbose`: Enable verbose output
- `--highlight`: Terms to highlight in the response (can specify multiple)

## Development Mode

For development and testing, you can enable DEBUG_MODE in your `.env` file:

```
DEBUG_MODE=true
```

In DEBUG_MODE:

- API key validation is bypassed
- A mock LLM is used instead of making real API calls
- Predefined responses are returned based on query patterns

This allows for easier development and testing without requiring valid API keys.

## Development

Check the `docs/` directory for detailed documentation on each component.

## Contributing

We welcome contributions to the Marketing Analyst Agent! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

For a comprehensive guide on project structure, documentation standards, and development workflow, refer to our [Project Maintenance Guide](docs/project_maintenance.md).

Also, please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
