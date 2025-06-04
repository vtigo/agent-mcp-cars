from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
from app.database.config import DATABASE_URL

# from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(DATABASE_URL, echo=True, future=True)

# Session = sessionmaker(engine)
def check_conn():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Connection with database confirmed.")
    except Exception as e:
        print(f"Failed to connect with to the database: {e}")
