from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    api_key=os.getenv("OPENAI_API_KEY"),  # type: ignore
    temperature=0,
)

# Import tools from tools.py to avoid duplication
from tools import calculator, get_current_time

tools = [calculator, get_current_time]

# Create the agent using LangChain 1.0's create_agent API
agent_app = create_agent(llm, tools)

# Export for use in main.py
def get_agent():
    return agent_app
