"""
Tests for the Marketing Analyst Agent.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from src.agents.marketing_analyst import MarketingAnalystAgent
from src.config import settings

# Skip tests if OPENAI_API_KEY is not set
pytestmark = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"), 
    reason="OPENAI_API_KEY environment variable not set"
)

class TestMarketingAnalystAgent:
    """Tests for the MarketingAnalystAgent class."""
    
    def setup_method(self):
        """Set up test environment before each test method."""
        # Use a mock for the LLM to avoid API calls during testing
        self.llm_patcher = patch('langchain_openai.ChatOpenAI')
        self.mock_llm = self.llm_patcher.start()
        self.mock_llm.return_value = MagicMock()
        
        # Mock tools
        self.tools_patcher = patch('src.agents.marketing_analyst.MarketingAnalystAgent._get_tools')
        self.mock_tools = self.tools_patcher.start()
        self.mock_tools.return_value = []
        
        # Create agent with mocked dependencies
        self.agent = MarketingAnalystAgent(
            model_name="gpt-3.5-turbo",
            enable_tracing=False,
            verbose=False
        )
        
        # Mock the agent executor
        self.agent.agent_executor = MagicMock()
        self.agent.agent_executor.invoke.return_value = {
            "output": "Mocked response from the marketing analyst agent",
            "some_other_key": "some_value"
        }
        
    def teardown_method(self):
        """Clean up after each test method."""
        self.llm_patcher.stop()
        self.tools_patcher.stop()
    
    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        assert self.agent is not None
        assert self.agent.model_name == "gpt-3.5-turbo"
        assert self.agent.enable_tracing is False
        assert self.agent.verbose is False
    
    def test_agent_run(self):
        """Test that the agent run method works correctly."""
        # Run the agent
        response = self.agent.run(query="Analyze market trends in the tech industry")
        
        # Check response
        assert isinstance(response, dict)
        assert "response" in response
        assert "success" in response
        assert response["response"] == "Mocked response from the marketing analyst agent"
        assert response["success"] is True
        
        # Verify the agent executor was called correctly
        self.agent.agent_executor.invoke.assert_called_once_with(
            {"input": "Analyze market trends in the tech industry"}
        )
    
    def test_agent_run_with_exception(self):
        """Test that the agent handles exceptions correctly."""
        # Set up the mock to raise an exception
        self.agent.agent_executor.invoke.side_effect = Exception("Test exception")
        
        # Run the agent
        response = self.agent.run(query="Analyze market trends in the tech industry")
        
        # Check response
        assert isinstance(response, dict)
        assert "response" in response
        assert "success" in response
        assert "An error occurred: Test exception" in response["response"]
        assert response["success"] is False 