import json
from langchain.tools import Tool
from app.mcp.client import send_mcp_command

def query_cars_tool_func(filters_json: str) -> str:
    """
    Send the action "get_cars" to the MCP server.
    - filters_json: a JSON string representing the filter criteria.
    The MCP server will handle validation, querying, and formatting a human-readable response.
    """
    try:
        json.loads(filters_json)
    except json.JSONDecodeError:
        return (
            "Invalid filters JSON. "
            "Example: {\"brand\": \"Ford\", \"model_year\": 2020}"
        )

    return send_mcp_command("get_cars", filters_json)

query_cars_tool = Tool(
    name="query_cars",
    func=query_cars_tool_func,
    description=(
        "Use this tool to search for cars in the database. "
        "Pass a JSON string of filters (e.g. '{\"brand\": \"Ford\", \"model_year\": 2020, \"color\": \"red\"}'). "
        "The available filters are: brand, model_name, model_year, category, color, price, fuel_type, door_count, transimission and safety_features"
        "The MCP server will return a human-readable list of matching cars, including all attributes."
    )
)
