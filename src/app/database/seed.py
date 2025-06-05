import random
from app.database.session import Session, engine
from app.models.car import Car, Base, CategoryEnum, ColorEnum, FuelTypeEnum, TransmissionEnum

brand_data = {
    "Toyota": ["Corolla", "Camry", "RAV4"],
    "Ford": ["Fiesta", "Focus", "Ranger"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Tesla": ["Model 3", "Model S", "Model X"],
    "Chevrolet": ["Cruze", "Malibu", "Trailblazer"],
    "Volkswagen": ["Golf", "Passat", "Tiguan"],
    "Hyundai": ["Elantra", "Tucson", "Santa Fe"],
    "BMW": ["320i", "X5", "M3"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLA"],
    "Nissan": ["Sentra", "Altima", "Frontier"]
}

safety_options = ["airbags", "abs", "lane_assist", "blind_spot_monitor"]

def generate_fake_car() -> Car:
    brand = random.choice(list(brand_data.keys()))
    model = random.choice(brand_data[brand])
    
    # select 1 - 4 safety features from the sample
    selected_features = random.sample(safety_options, k=random.randint(1, len(safety_options)))
    # join them by a ","
    safety_features =",".join(selected_features) 

    return Car(
        brand=brand,
        model_name=model,
        category=random.choice(list(CategoryEnum)).value,
        fuel_type=random.choice(list(FuelTypeEnum)).value,
        model_year=random.randint(2000, 2024),
        color=random.choice(list(ColorEnum)).value,
        price=random.randint(50000, 250000),
        door_count=random.choice([2, 4, 5]),
        transmission=random.choice(list(TransmissionEnum)).value,
        safety_features=safety_features
    )

def seed_data():
    """Seed """
    Base.metadata.create_all(engine)
    
    with Session() as session:
        # Calculate how many cars to seed to reach 100 cars in the database
        existing_cars_count = session.query(Car).count()
        seed_count = 100 - existing_cars_count

        if seed_count < 1:
            print("Database already seeded. Skipping.")
            return

        print(f"Seeding {seed_count} cars...")
        cars = [generate_fake_car() for _ in range(seed_count)]
        session.add_all(cars)
        session.commit()
        print("Done seeding.")

def wipe_data():
    with Session() as session:
        print("Wiping the db clean...")
        session.query(Car).delete()
        session.commit()
        print("Done wiping.")
