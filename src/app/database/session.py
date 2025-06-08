from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from app.database.config import DATABASE_URL

load_dotenv()

engine = create_engine(DATABASE_URL, future=True)
Session = sessionmaker(engine)

def check_database_connection() ->  bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return True
    except Exception as e:
        return False
