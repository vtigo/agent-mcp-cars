from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()  # Load TOGETHER_API_KEY from .env

# Initialize the model
model = init_chat_model("meta-llama/Llama-3.3-70B-Instruct-Turbo", model_provider="together", max_tokens=50)

def send_prompt(prompt: str) -> str:
    """Send a prompt to initialized model and return the response."""
    try:
        response = model.invoke(prompt).content
        return str(response)
    except Exception as e:
        return f"[Failed to invoke the model]: {e}"
