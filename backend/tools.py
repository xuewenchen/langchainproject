from langchain.tools import tool
from datetime import datetime

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
