from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent, ToolNode
from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import MessagesPlaceholder
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
import os
import operator
from datetime import datetime

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    api_key=os.getenv("OPENAI_API_KEY"), # type: ignore
    temperature=0
)

@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Args:
        expression: A mathematical expression as a string, e.g., "2 + 3 * 4"

    Returns:
        The result of the calculation as a string
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_current_time() -> str:
    """
    Get the current date and time.

    Returns:
        The current date and time as a string
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

tools = [calculator, get_current_time]

app = create_react_agent(llm, tools)

async def create_agent():
    return app
