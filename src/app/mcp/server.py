import json
import socket
import threading
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import Session 
from app.models.car import Car

HOST = "127.0.0.1"
PORT = 3333

import json
from sqlalchemy.exc import SQLAlchemyError

def handle_request(conn, addr):
    # TODO: deal with addr
    with conn:
        try:
            data = conn.recv(4096)
            if not data:
                return

            # Decode JSON
            try:
                request = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON")

            # Extract action
            action = request.get("action")
            if action == "get_cars":
                # Ensure filters is a dict, default to {}
                filters = request.get("filters", {})
                if not isinstance(filters, dict):
                    raise ValueError("“filters” must be a JSON object")

                # Return [] if no rows match
                results = query_cars(filters)
                response = {"status": "ok", "results": results}

            else:
                response = {"status": "error", "message": f"Unknown action: {action}"}

        except ValueError as ve:
            response = {"status": "error", "message": str(ve)}

        except SQLAlchemyError as e:
            response = {"status": "error", "message": f"Database Error: {e}"}

        except Exception as e:
            response = {"status": "error", "message": str(e)}

        # Send back a JSON with the response
        conn.sendall(json.dumps(response).encode("utf-8"))


def query_cars(filters: dict) -> list:
    """
    - filters: a dict whose keys correspond to Car model columns
      (e.g. "brand", "model_name", "model_year", "color", etc.).
    - If filters is empty ({}), this will return [] (no cars).
    """

    # Build clean_filters: only keep non‐empty values that match Car attributes
    clean_filters = {}
    for key, val in filters.items():
        # ignore None or empty‐string filters
        if val is None or (isinstance(val, str) and val.strip() == ""):
            continue

        # look for matching collums (only allow columns that actually exist on Car)
        if hasattr(Car, key):
            clean_filters[key] = val

    # Return [] to avoid errors
    if not clean_filters:
        return []

    with Session() as session:
        try:
            query = session.query(Car).filter_by(**clean_filters)
            results = query.all()
        except SQLAlchemyError:
            # Let the caller deal with it :)
            raise

    return [
            {
                "id":              c.id,
                "brand":           c.brand,
                "model_name":      c.model_name,
                "model_year":      c.model_year,
                "color":           c.color,
                "category":        c.category,
                "fuel_type":       c.fuel_type,
                "door_count":      c.door_count,
                "transmission":    c.transmission,
                "price":           c.price,
                "safety_features": c.safety_features,
                }
            for c in results
            ]

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"MCP server running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.daemon = True
            thread.start()
