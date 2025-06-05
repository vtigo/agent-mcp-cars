from sqlalchemy.orm import Session
from app.models.car import Car
from app.database.session import engine

def read_all_cars():
    with Session(engine) as session:
        cars = session.query(Car).all()
        for car in cars:
            print(car)

if __name__ == "__main__":
    read_all_cars()

