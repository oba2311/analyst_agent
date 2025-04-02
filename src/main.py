"""
Main entry point for the Marketing Analyst Agent.

This module initializes and runs the marketing analyst agent.
"""

import logging
import argparse
import sys
from typing import Dict, Any, Optional, List

from src.agents.marketing_analyst import MarketingAnalystAgent
from src.config import settings
from src.utils.formatting import format_cli_response, highlight_text

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def validate_environment() -> bool:
    """
    Validate that all required environment variables are set.
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
    issues = settings.validate_env()
    
    if issues:
        logger.error("Environment validation failed:")
        for key, message in issues.items():
            logger.error(f"  - {key}: {message}")
        return False
    
    return True

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Marketing Analyst Agent")
    
    parser.add_argument(
        "--model", 
        type=str, 
        default=settings.DEFAULT_MODEL,
        help=f"OpenAI model to use (default: {settings.DEFAULT_MODEL})"
    )
    
    parser.add_argument(
        "--query", 
        type=str, 
        help="Query to run (if not provided, interactive mode will be used)"
    )
    
    parser.add_argument(
        "--no-tracing", 
        action="store_true",
        help="Disable LangSmith tracing"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--highlight", 
        type=str,
        nargs="*",
        help="Terms to highlight in the output"
    )
    
    return parser.parse_args()

def run_interactive_mode(agent: MarketingAnalystAgent, highlight_terms: Optional[List[str]] = None) -> None:
    """
    Run the agent in interactive mode.
    
    Args:
        agent: The marketing analyst agent instance
        highlight_terms: Optional terms to highlight in responses
    """
    print("\n===== Marketing Analyst Agent (Interactive Mode) =====")
    print("Enter your queries and get marketing insights.")
    print("Type 'exit', 'quit', or 'q' to exit.")
    print("=================================================\n")
    
    while True:
        try:
            query = input("\nEnter your query: ")
            
            if query.lower() in ["exit", "quit", "q"]:
                print("Exiting...")
                break
                
            if not query.strip():
                continue
                
            print("\nProcessing query...")
            response = agent.run(query)
            
            formatted_response = format_cli_response(response["response"])
            if highlight_terms:
                formatted_response = highlight_text(formatted_response, highlight_terms)
                
            print("\nResponse:")
            print(formatted_response)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            print(f"\nAn error occurred: {str(e)}")

def main() -> int:
    """
    Main function to run the marketing analyst agent.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Validate environment
    if not validate_environment():
        return 1
    
    logger.info(f"Initializing Marketing Analyst Agent with model: {args.model}")
    
    try:
        # Initialize the agent
        agent = MarketingAnalystAgent(
            model_name=args.model,
            enable_tracing=not args.no_tracing,
            verbose=args.verbose
        )
        
        # Run query or interactive mode
        if args.query:
            logger.info(f"Running query: {args.query}")
            response = agent.run(query=args.query)
            
            formatted_response = format_cli_response(response["response"])
            if args.highlight:
                formatted_response = highlight_text(formatted_response, args.highlight)
                
            print(formatted_response)
        else:
            run_interactive_mode(agent, args.highlight)
            
        return 0
    
    except Exception as e:
        logger.error(f"Error running agent: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 