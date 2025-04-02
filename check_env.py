#!/usr/bin/env python3
"""
Check for environment variables that might conflict with your .env file.
This script prints out any environment variables related to OpenAI or LangChain
that are already set in your system environment.
"""

import os
import sys
from dotenv import load_dotenv

def check_env_conflicts():
    """Check for environment variables that might conflict with .env settings."""
    # List of environment variables to check
    vars_to_check = [
        # OpenAI related
        "OPENAI_API_KEY",
        "OPENAI_ORGANIZATION",
        "OPENAI_API_BASE",
        "OPENAI_API_TYPE",
        "OPENAI_API_VERSION",
        
        # Azure OpenAI related
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_VERSION",
        
        # LangChain related
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_ENDPOINT",
        "LANGCHAIN_TRACING",
        "LANGCHAIN_PROJECT",
        "LANGSMITH_API_KEY",
        "LANGSMITH_ENDPOINT",
        "LANGSMITH_PROJECT",
        "LANGSMITH_TRACING",
    ]
    
    print("=== Environment Variables Before Loading .env File ===")
    
    # Check each variable before loading .env
    env_vars_before = {}
    for var in vars_to_check:
        value = os.environ.get(var)
        if value:
            # Mask API keys for security
            if "API_KEY" in var and value:
                masked_value = value[:10] + "..." + value[-5:] if len(value) > 15 else "***"
                env_vars_before[var] = masked_value
            else:
                env_vars_before[var] = value
    
    # Print results for pre-.env check
    if env_vars_before:
        print("Found the following environment variables already set:")
        for var, value in env_vars_before.items():
            print(f"  {var}: {value}")
    else:
        print("No relevant environment variables found in your system environment.")
    
    # Now load the .env file
    print("\n=== Loading .env File ===")
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(dotenv_path):
        print(f"Found .env file at: {dotenv_path}")
        # Load without override to see what would happen normally
        load_dotenv(dotenv_path, override=False)
        
        # Check what variables are now set
        print("\n=== Environment Variables After Loading .env (without override) ===")
        for var in vars_to_check:
            value = os.environ.get(var)
            if value:
                # Mask API keys for security
                if "API_KEY" in var and value:
                    masked_value = value[:10] + "..." + value[-5:] if len(value) > 15 else "***"
                    if var in env_vars_before and env_vars_before[var] != masked_value:
                        print(f"  {var}: {masked_value} (CONFLICT! Original value was kept)")
                    else:
                        print(f"  {var}: {masked_value}")
                else:
                    if var in env_vars_before and env_vars_before[var] != value:
                        print(f"  {var}: {value} (CONFLICT! Original value was kept)")
                    else:
                        print(f"  {var}: {value}")
        
        # Now load with override
        load_dotenv(dotenv_path, override=True)
        
        # Check what variables are now set
        print("\n=== Environment Variables After Loading .env (with override=True) ===")
        for var in vars_to_check:
            value = os.environ.get(var)
            if value:
                # Mask API keys for security
                if "API_KEY" in var and value:
                    masked_value = value[:10] + "..." + value[-5:] if len(value) > 15 else "***"
                    if var in env_vars_before and env_vars_before[var] != masked_value:
                        print(f"  {var}: {masked_value} (OVERRIDDEN from original value)")
                    else:
                        print(f"  {var}: {masked_value}")
                else:
                    if var in env_vars_before and env_vars_before[var] != value:
                        print(f"  {var}: {value} (OVERRIDDEN from original value)")
                    else:
                        print(f"  {var}: {value}")
    else:
        print(f"No .env file found at: {dotenv_path}")
    
    print("\n=== Recommendations ===")
    if env_vars_before:
        print("You have conflicting environment variables set in your system that may override your .env file.")
        print("Options to fix this:")
        print("1. Use 'load_dotenv(override=True)' in your scripts")
        print("2. Explicitly unset the conflicting environment variables:")
        for var in env_vars_before:
            if sys.platform == 'win32':
                print(f"   - Windows: set {var}=")
            else:
                print(f"   - Unix/Mac: unset {var}")
        print("3. Explicitly set variables in your code: os.environ['VAR_NAME'] = 'value'")
    else:
        print("No conflicts detected. Your .env file should work as expected.")
    
if __name__ == "__main__":
    check_env_conflicts() 