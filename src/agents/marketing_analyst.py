"""
Marketing Analyst Agent Implementation.

This module implements the core marketing analyst agent using LangChain components.
"""

from typing import Dict, List, Any, Optional
import logging

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.base import BaseTool
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import Runnable, RunnablePassthrough
from langchain.schema.messages import SystemMessage, HumanMessage, AIMessage
from langchain.schema.output import LLMResult
from langchain.llms.base import LLM
from langsmith import Client as LangSmithClient

from src.config import settings
from src.tools.market_data import (
    MarketTrendAnalysisTool,
    CompetitorAnalysisTool,
    ConsumerSentimentTool
)
from src.tools.report import ReportGenerationTool
from src.tools.strategy import StrategyRecommendationTool

# Configure logging
logger = logging.getLogger(__name__)

# System prompt for the marketing analyst agent
MARKETING_ANALYST_SYSTEM_PROMPT = """You are an expert marketing analyst AI assistant. 
Your job is to analyze marketing data, identify trends, evaluate campaign performance, 
and provide strategic recommendations based on data-driven insights.

Follow these principles in your analysis:
1. Always ground your analysis in data
2. Consider multiple angles before drawing conclusions
3. Be aware of market context and industry trends
4. Consider both short-term tactics and long-term strategy
5. Provide clear, actionable recommendations
6. Explain your reasoning and methodology

You have access to various tools that can help you analyze marketing data and generate insights.
"""

# Mock LLM for debug mode
class MockLLM(LLM):
    """A mock LLM that returns predefined responses for debugging purposes."""
    
    def _call(self, prompt: str, **kwargs) -> str:
        """Return a mock response."""
        logger.info(f"DEBUG MODE: Using mock LLM response for prompt: {prompt[:100]}...")
        
        # Return a simple response that just tells the user what tools would be used
        if "mobile gaming" in prompt.lower():
            return """Based on the market trend analysis tool, here are the key trends in the mobile gaming market:

1. Increasing mobile engagement - More users are spending longer sessions on mobile games, with average session times increasing by 15% year over year.

2. Greater emphasis on sustainability - Game developers are focusing on sustainable monetization models that prioritize player retention over short-term revenue.

3. Shift toward personalized experiences - Games are increasingly using player data to create customized gameplay experiences and recommendations.

4. Integration of AI-driven analytics - Developers are leveraging AI tools to understand player behavior and optimize game mechanics.

The mobile gaming market has shown a growth rate of 12.5% over the past year, with a current market size of $8.7 billion. This growth is expected to continue as mobile devices become more powerful and 5G adoption increases.
"""
        elif "competitor" in prompt.lower():
            return "I would analyze this using the competitor analysis tool to provide insights on market positioning, strengths, and weaknesses."
        elif "sentiment" in prompt.lower():
            return "I would use the consumer sentiment analysis tool to evaluate how users feel about this product across different channels."
        elif "report" in prompt.lower():
            return "I would generate a comprehensive report using the report generation tool with the sections you requested."
        elif "strategy" in prompt.lower() or "recommend" in prompt.lower():
            return "I would develop strategic recommendations using the strategy recommendation tool based on your business objectives."
        else:
            return "I'd need to analyze this request further. Could you provide more details about what specific marketing insights you're looking for?"
    
    @property
    def _llm_type(self) -> str:
        return "mock_llm"

class MarketingAnalystAgent:
    """
    Marketing Analyst Agent implementation using LangChain components.
    """
    
    def __init__(
        self,
        model_name: str = settings.DEFAULT_MODEL,
        enable_tracing: bool = settings.ENABLE_TRACING,
        verbose: bool = True
    ):
        """
        Initialize the Marketing Analyst Agent.
        
        Args:
            model_name: The name of the OpenAI model to use
            enable_tracing: Whether to enable LangSmith tracing
            verbose: Whether to enable verbose logging
        """
        self.model_name = model_name
        self.enable_tracing = enable_tracing
        self.verbose = verbose
        
        # Initialize LangSmith client if tracing is enabled and not in debug mode
        if self.enable_tracing and not settings.DEBUG_MODE:
            if settings.LANGSMITH_API_KEY:
                self.langsmith_client = LangSmithClient()
            else:
                logger.warning("LangSmith API key not provided, tracing disabled")
                self.enable_tracing = False
        
        # Initialize the agent components
        self._setup_agent()
    
    def _setup_agent(self) -> None:
        """Set up the agent with tools, prompt, and memory."""
        # Initialize the language model
        model_kwargs = settings.get_model_kwargs()
        
        # Use mock LLM in debug mode
        if settings.DEBUG_MODE:
            logger.info("Running in DEBUG MODE with mock LLM")
            self.llm = MockLLM()
        else:
            self.llm = ChatOpenAI(
                model=self.model_name,
                temperature=model_kwargs["temperature"],
                max_tokens=model_kwargs["max_tokens"],
                api_key=settings.OPENAI_API_KEY,
            )
        
        # Initialize the tools
        self.tools = self._get_tools()
        
        # Initialize the memory - using the newer format to avoid deprecation warning
        self.memory = ConversationBufferMemory(
            return_messages=True,
            input_key="input",
            output_key="output",
            memory_key="chat_history"
        )
        
        # Initialize the prompt
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=MARKETING_ANALYST_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent (simplified in DEBUG_MODE)
        if settings.DEBUG_MODE:
            # In DEBUG mode, we'll skip the OpenAI functions agent creation
            # and create a simple agent executor that just runs the mock LLM
            self.agent = RunnablePassthrough()
            self.agent_executor = self._create_debug_agent_executor()
        else:
            # Normal agent setup
            self.agent = create_openai_functions_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=self.prompt
            )
            
            # Create the agent executor
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                memory=self.memory,
                verbose=self.verbose,
                handle_parsing_errors=True,
            )
    
    def _create_debug_agent_executor(self):
        """Create a simplified agent executor for debug mode that just calls the mock LLM."""
        
        def simple_executor(inputs):
            query = inputs.get("input", "")
            # Use invoke() instead of __call__ to avoid deprecation warning
            response = self.llm.invoke(query)
            return {"output": response}
            
        return simple_executor
    
    def _get_tools(self) -> List[BaseTool]:
        """
        Get the tools available to the agent.
        
        Returns:
            List[BaseTool]: List of tools
        """
        return [
            MarketTrendAnalysisTool(),
            CompetitorAnalysisTool(),
            ConsumerSentimentTool(),
            ReportGenerationTool(),
            StrategyRecommendationTool(),
        ]
    
    def run(self, input_text: str = None, query: str = None) -> Dict[str, Any]:
        """
        Run the agent on the given input.
        
        Args:
            input_text: The input query or request (deprecated)
            query: The query to process (preferred)
            
        Returns:
            Dict[str, Any]: The agent's response
        """
        try:
            # Use query parameter if provided, otherwise use input_text
            final_query = query if query is not None else input_text
            
            # Run the agent
            response = self.agent_executor.invoke({"input": final_query})
            return {
                "response": response["output"],
                "success": True
            }
        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            return {
                "response": f"An error occurred: {str(e)}",
                "success": False
            } 