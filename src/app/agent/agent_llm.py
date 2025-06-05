from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from app.agent.tools import query_cars_tool

load_dotenv()

# Initialize the language model
model = init_chat_model(
        "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        model_provider="together",
        max_tokens=512
        )

# Define the system prompt
system_prompt = (
        "You are Mick, a helpful assistant specialized in searching a cars database.\n"
        "If the user’s question does not require any database lookup, respond with plain natural language only — no JSON or function call objects.\n\n"
        "When the user asks for specific types of cars (e.g. by brand, color, year), "
        "you must extract filters and use the `query_cars_tool` to search the database. "
        "When the tool returns results, read the output and write a helpful response based on it.\n\n"

        "If the user's question is general (e.g. about engines, car types, or concepts), answer directly, without invoking any tool.\n\n"

        "=== Examples ===\n\n"

        "User: I want a white car from Nissan.\n"
        "Thought: The user wants specific cars. I will call the tool with the appropriate filters.\n"
        "Action: query_cars_tool\n"
        "Action Input: {\"brand\": \"Nissan\", \"color\": \"white\"}\n"
        "Observation: Found 2 car(s):\n"
        "- Nissan Versa (2020), white, flex, automatic, 4 doors, R$50000\n"
        "- Nissan Kicks (2021), white, flex, automatic, 4 doors, R$62000\n"
        "Final Answer: Here are two white Nissan cars I found:\n"
        "- Versa (2020) for R$50000\n"
        "- Kicks (2021) for R$62000\n\n"

        "User: How does an electric engine work?\n"
        "Thought: The user is asking a general knowledge question. No need to use the database.\n"
        "Final Answer: An electric engine uses electromagnetic fields to generate motion. It typically includes a motor, battery, and control system that work together to convert electrical energy into mechanical energy.\n\n"

        "User: I want a 4-door black SUV with automatic transmission.\n"
        "Thought: The user is looking for a specific type of car. I will call the query_cars_tool.\n"
        "Action: query_cars_tool\n"
        "Action Input: {\"category\": \"suv\", \"color\": \"black\", \"door_count\": 4, \"transmission\": \"automatic\"}\n"
        "Observation: Found 1 car:\n"
        "- Toyota SW4 (2022), black, diesel, automatic, 4 doors, R$240000\n"
        "Final Answer: I found one black 4-door SUV with automatic transmission:\n"
        "- Toyota SW4 (2022), diesel, R$240000\n\n"

        "=== End of Examples ===\n\n"

        "Always reason step-by-step and clearly decide whether to use the tool.\n"
        "After the tool returns the result, write a concise answer that summarizes "
        "how many matches were found, and list every car."
        )

agent = create_react_agent(
        model=model,
        tools=[query_cars_tool],
        prompt=system_prompt
        )

def send_prompt(prompt: str) -> str:
    """
    Sends a prompt to the initialized agent and returns the final AI response.
    """
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        messages = result.get("messages", [])

        # Reverse iterate through message objects and extract valid AI responses
        for msg in reversed(messages):
            if getattr(msg, "type", None) == "ai" and getattr(msg, "content", "").strip():
                return msg.content

        return "[No Valid AI response]"
    except Exception as e:
        return f"[AGENT ERROR]: {e}"

