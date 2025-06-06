import os
import json
import socket
from dotenv  import load_dotenv

load_dotenv()

MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("MCP_PORT", 3333))

def send_mcp_command(action: str, filters_json: str, host=MCP_HOST, port=MCP_PORT, timeout=5) -> str:
    try:
        filters = json.loads(filters_json)
        request = {
            "action": action,
            "filters": filters
        }

        with socket.create_connection((host, port), timeout=timeout) as conn:
            conn.sendall(json.dumps(request).encode("utf-8"))
            data = conn.recv(8192)

        return data.decode("utf-8")

    except json.JSONDecodeError:
        return "[MCP CLIENT ERROR]: Invalid JSON filters input."

    except ConnectionRefusedError:
        return "[MCP CLIENT ERROR]: MCP server is offline or unreachable."

    except Exception as e:
        return f"[MCP CLIENT ERROR]: {str(e)}"
