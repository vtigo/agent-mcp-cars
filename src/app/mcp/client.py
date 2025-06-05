import json
import socket

HOST = "127.0.0.1"
PORT = 3333

def send_get_cars_request(filters: dict) -> dict:
    request = {
        "action": "get_cars",
        "filters": filters
    }
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(json.dumps(request).encode("utf-8"))
            data = s.recv(8192)
            response = json.loads(data.decode("utf-8"))
            return response
    except ConnectionRefusedError:
        return {"status": "error", "message": "MCP server offline ou unreachable"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
