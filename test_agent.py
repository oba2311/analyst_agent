"""
Simple test script for the Marketing Analyst Agent in debug mode.
"""
import os

# Set debug mode in environment
os.environ["DEBUG_MODE"] = "true"

from src.agents.marketing_analyst import MarketingAnalystAgent

def main():
    """Run a simple test of the marketing analyst agent."""
    print("Initializing Marketing Analyst Agent in DEBUG mode...")
    agent = MarketingAnalystAgent(verbose=True)
    
    # Test query
    query = "What are the key trends in the mobile gaming market?"
    print(f"\nQuery: {query}")
    print("\nProcessing...")
    
    response = agent.run(query=query)
    
    print("\nResponse:")
    print(response["response"])
    
    return 0

if __name__ == "__main__":
    main() 