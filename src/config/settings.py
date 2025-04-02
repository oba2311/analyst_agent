"""
Environment and configuration settings for the Marketing Analyst Agent.
"""

import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "marketing_analyst_agent")

# Agent Configuration
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4")
AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.2"))
AGENT_MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS", "2000"))

# Storage Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///marketing_agent.db")

# Feature Flags
ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"

# Debug Mode - set to True to bypass API key validation
DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"

# Check if required environment variables are set
def validate_env() -> Dict[str, str]:
    """
    Validate that all required environment variables are set.
    
    Returns:
        Dict[str, str]: Dictionary of missing or invalid environment variables
    """
    issues = {}
    
    # Skip validation if in DEBUG_MODE
    if DEBUG_MODE:
        return issues
    
    if not OPENAI_API_KEY:
        issues["OPENAI_API_KEY"] = "Missing OpenAI API key"
    
    if ENABLE_TRACING and not LANGSMITH_API_KEY:
        issues["LANGSMITH_API_KEY"] = "LangSmith API key required when tracing is enabled"
    
    return issues

def get_model_kwargs() -> Dict[str, Any]:
    """
    Get keyword arguments for the language model.
    
    Returns:
        Dict[str, Any]: Dictionary of model configuration parameters
    """
    return {
        "temperature": AGENT_TEMPERATURE,
        "max_tokens": AGENT_MAX_TOKENS,
    } 