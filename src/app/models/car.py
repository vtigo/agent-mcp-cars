import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class CategoryEnum(str, enum.Enum):
    sedan = "sedan"
    suv = "suv"
    truck = "truck"

class FuelTypeEnum(str, enum.Enum):
    gasoline = "gasoline"
    diesel = "diesel"
    electric = "electric"
    flex = "flex"

class ColorEnum(str, enum.Enum):
    black = "black"
    white = "white"
    silver = "silver"
    red = "red"

class TransmissionEnum(str, enum.Enum):
    automatic = "automatic"
    manual = "manual"

class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(50))
    model_name: Mapped[str] = mapped_column(String(50))
    category: Mapped[CategoryEnum] = mapped_column(Enum(CategoryEnum), nullable=False)
    fuel_type: Mapped[FuelTypeEnum] = mapped_column(Enum(FuelTypeEnum), nullable=False)
    model_year: Mapped[int]
    color: Mapped[ColorEnum] = mapped_column(Enum(ColorEnum), nullable=False)
    price: Mapped[int]
    door_count: Mapped[int]
    transmission: Mapped[TransmissionEnum] = mapped_column(Enum(TransmissionEnum), nullable=False)
    safety_features: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        def val(v): return v.value if isinstance(v, enum.Enum) else v

        return (
            f"Car(id={self.id}, brand={self.brand}, model_name={self.model_name}, "
            f"category={val(self.category)}, fuel_type={val(self.fuel_type)}, "
            f"year={self.model_year}, color={val(self.color)}, "
            f"price={self.price}, doors={self.door_count}, "
            f"transmission={val(self.transmission)}, safety_features={self.safety_features})"
        )

