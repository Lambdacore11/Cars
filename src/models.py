from decimal import Decimal
from sqlmodel import SQLModel, CheckConstraint, Field, Relationship
from pydantic import field_validator
from .schemas import CAR_NAME_SCHEMA, CAR_COLOR_SCHEMA, MANUFACTURER_NAME_SCHEMA


class ManufacturerBase(SQLModel):
    name: str = Field(
        index=True, max_length=50,
        schema_extra=MANUFACTURER_NAME_SCHEMA
    )

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v

class Manufacturer(ManufacturerBase, table=True):
    __tablename__ = 'manufacturers'
    id: int | None = Field(default=None, primary_key=True)
    cars: list['Car'] = Relationship(back_populates="manufacturer")

    __table_args__ = (
        CheckConstraint(
            "name ~ '^[a-zA-Z\\-]+$'",
            name='check_manufacturer_name_regex'
        ),
    )

class ManufacturerPublic(ManufacturerBase):
    id : int

class ManufacturerCreate(ManufacturerBase):
    pass

class ManufacturerUpdate(SQLModel):
    name: str | None = Field(
        default=None, max_length=50,
        schema_extra=MANUFACTURER_NAME_SCHEMA
    )

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if v is not None and isinstance(v, str):
            return v.lower().strip()
        return v


class CarBase(SQLModel):
    name: str = Field(
        index=True,
        max_length=50,
        schema_extra=CAR_NAME_SCHEMA
    )
    color: str = Field(
        index=True,
        max_length=50,
        schema_extra=CAR_COLOR_SCHEMA
    )
    price: Decimal = Field(
        default=0,
        max_digits=11,
        decimal_places=2,
        ge=Decimal('0'))

    @field_validator('name','color', mode='before')
    @classmethod
    def validate_name(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v

class Car(CarBase, table=True):
    __tablename__ = 'cars'
    id: int | None = Field(
        default=None,
        primary_key=True
    )
    manufacturer_id: int = Field(
        foreign_key='manufacturers.id',
        ondelete='CASCADE'
    )
    manufacturer: Manufacturer = Relationship(back_populates='cars')

    __table_args__ = (
        CheckConstraint("name ~ '^[a-zA-Z0-9\\-]+$'", name='check_car_name_regex'),
        CheckConstraint("color ~ '^[a-zA-Z\\-]+$'", name='check_car_color_regex'),
        CheckConstraint('price >= 0', name='check_price_positive'),
    )

class CarPublic(CarBase):
    id: int
    manufacturer_id : int
    manufacturer_name: str

class CarCreate(CarBase):
    manufacturer_name: str = Field(
        max_length=50,
        schema_extra=MANUFACTURER_NAME_SCHEMA
    )

    @field_validator('manufacturer_name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v

class CarUpdate(SQLModel):
    name: str | None = Field(
        default=None, max_length=50,
        schema_extra=CAR_NAME_SCHEMA
    )
    color: str | None = Field(
        default=None, max_length=50,
        schema_extra=CAR_COLOR_SCHEMA
    )
    price: Decimal | None = Field(
        default=None, max_digits=11,
        decimal_places=2,
        ge=Decimal('0')
    )
    manufacturer_name: str | None = Field(
        default=None,
        max_length=50,
        schema_extra=MANUFACTURER_NAME_SCHEMA
    )

    @field_validator('name', 'color', 'manufacturer_name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if v is not None and isinstance(v, str):
            return v.lower().strip()
        return v
