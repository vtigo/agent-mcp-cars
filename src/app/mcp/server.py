import json
import socket
import threading
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import Session 
from app.models.car import Car

HOST = "127.0.0.1"
PORT = 3333

def handle_connection(conn):
    with conn:
        try:
            data = conn.recv(4096)
            if not data:
                return

            request = json.loads(data.decode("utf-8"))

            action = request.get("action")
            if action == "get_cars":
                filters = request.get("filters", {})
                results = query_cars(filters)
                response = {"status": "ok", "results": results}
            else:
                response = {"status": "error", "message": f"Unknown action: {action}"}
                
        except (json.JSONDecodeError, KeyError):
            response = {"status": "error", "message": "Invalid JSON"}
        except SQLAlchemyError as e:
            response = {"status": "error", "message": f"Database Error: {e}"}
        except Exception as e:
            response = {"status": "error", "message": str(e)}

        conn.sendall(json.dumps(response).encode("utf-8"))

def query_cars(filters: dict) -> list:
    filter_keys = [
        "brand",
        "model_name",
        "model_year",
        "color",
        "category",
        "fuel_type",
        "door_count",
        "transmission",
        "price",
        "safety_features",
    ]

    with Session() as session:
        query = session.query(Car)

        for key in filter_keys:
            val = filters.get(key)
            if val is not None and val != "":
                query = query.filter(getattr(Car, key) == val)

        results = query.all()

    return [
        {
            "id":               car.id,
            "brand":            car.brand,
            "model_name":       car.model_name,
            "model_year":       car.model_year,
            "color":            car.color,
            "category":         car.category,
            "fuel_type":        car.fuel_type,
            "door_count":       car.door_count,
            "transmission":     car.transmission,
            "price":            car.price,
            "safety_features":  car.safety_features,
        }
        for car in results
    ]

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"MCP server running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_connection, args=(conn, addr))
            thread.daemon = True
            thread.start()

if __name__  == "__main__":
    run_server()
