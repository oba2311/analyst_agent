# Description: Test script to verify the OpenAI API key and model configuration.
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Clear any existing environment variable and set the one from .env
os.environ["OPENAI_API_KEY"] = api_key

# Create LLM with explicit API key
llm = ChatOpenAI(api_key=api_key)

# Verify the model's organization/type
print(f"Model configuration: {llm.model_name}")

# Invoke the model
response = llm.invoke("Hello, world!")
print("Response:", response)
