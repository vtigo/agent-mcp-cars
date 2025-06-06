import os
import json
import socket
import threading
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import Session 
from app.models.car import Car

load_dotenv()

MCP_HOST = os.getenv("MCP_HOST", "127.0.0.1")
MCP_PORT = int(os.getenv("MCP_PORT", 3333))

def handle_request(conn, addr):
    """
    Receives a JSON payload {"action": "...", "filters": {...}},
    executes the corresponding command, and returns a plain-text response
    that includes all attributes for each matching Car.
    """
    with conn:
        try:
            data = conn.recv(4096)
            if not data:
                return
            
            # Decode incoming JSON
            try:
                request = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON request")

            # Retrieve the action and do the necessary operations
            action = request.get("action")
            if action == "get_cars":
                # Validate filters
                filters = request.get("filters", {})
                if not isinstance(filters, dict):
                    raise ValueError("“filters” must be a JSON object (dict)")

                # Query the database
                cars = query_cars(filters)

                # Build the response
                if not cars:
                    response_str = "No cars found for the given filters."
                else:
                    lines = []
                    for c in cars:
                        lines.append(
                                f"- ID: {c['id']}, "
                                f"Brand: {c['brand']}, "
                                f"Model: {c['model_name']}, "
                                f"Year: {c['model_year']}, "
                                f"Color: {c['color']}, "
                                f"Category: {c['category']}, "
                                f"Fuel: {c['fuel_type']}, "
                                f"Doors: {c['door_count']}, "
                                f"Transmission: {c['transmission']}, "
                                f"Price: R${c['price']}, "
                                f"Safety Features: {c['safety_features']}"
                                )
                    response_str = "Found {} car(s):\n{}".format(len(cars), "\n".join(lines))

            else:
                response_str = f"Unknown action: {action}"

        except ValueError as e:
            response_str = f"[MCP SERVER ERROR]: {e}"

        except SQLAlchemyError as e:
            response_str = f"[MCP SERVER ERROR]: Database Error: {e}"

        except Exception as e:
            response_str = f"[MCP SERVER ERROR]: {e}"

        # Send back a plain text response
        conn.sendall(response_str.encode("utf-8"))


def query_cars(filters: dict) -> list:
    """
    - filters: a dict whose keys correspond to Car model columns
      (e.g. "brand", "model_name", "model_year", "color", etc.).
    - If filters is empty ({}), this will return [] (no cars).
    """

    # We only want non‐empty filter values that match Car attributes
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
                "id": c.id,
                "brand": c.brand,
                "model_name": c.model_name,
                "model_year": c.model_year,
                "color": c.color,
                "category": c.category,
                "fuel_type": c.fuel_type,
                "door_count": c.door_count,
                "transmission": c.transmission,
                "price": c.price,
                "safety_features": c.safety_features,
                }
            for c in results
            ]

def run_server():
    """Start the MCP server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((MCP_HOST,MCP_PORT))
        s.listen()
        print(f"MCP server running on {MCP_HOST}:{MCP_PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.daemon = True
            thread.start()
