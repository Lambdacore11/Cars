'''Models module'''
from decimal import Decimal
from sqlmodel import SQLModel, CheckConstraint, Field, Relationship, \
                        UniqueConstraint
from sqlalchemy import event
from .schemas import CAR_NAME_SCHEMA, CAR_COLOR_SCHEMA, \
                        MANUFACTURER_NAME_SCHEMA


class ManufacturerBase(SQLModel):
    '''Base class for Manufacturer'''
    name: str = Field(
        index=True,
        max_length=50,
        schema_extra=MANUFACTURER_NAME_SCHEMA
    )


class Manufacturer(ManufacturerBase, table=True):
    '''Database representation for Manufacturer'''
    __tablename__ = 'manufacturers'

    id: int | None = Field(default=None, primary_key=True)
    cars: list['Car'] = Relationship(back_populates="manufacturer")

    __table_args__ = (
        UniqueConstraint('name', name='check_manufacturer_unique_name'),
    )


class ManufacturerPublic(ManufacturerBase):
    '''Public class for Manufacturer'''
    id: int


class ManufacturerCreate(ManufacturerBase):
    '''Class for Manufacturer creation'''


class ManufacturerUpdate(SQLModel):
    '''Class for uupdate Manufacturer'''
    name: str | None = Field(
        default=None, max_length=50,
        schema_extra=MANUFACTURER_NAME_SCHEMA
    )


class CarBase(SQLModel):
    '''Base class for Car'''
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


class Car(CarBase, table=True):
    '''Database representation for Car'''
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
        CheckConstraint('price >= 0', name='check_price_positive'),
    )


class CarPublic(CarBase):
    '''Public class for Car'''
    id: int
    manufacturer_id: int
    manufacturer_name: str


class CarCreate(CarBase):
    '''Class for Car creation'''
    manufacturer_name: str = Field(
        max_length=50,
        schema_extra=MANUFACTURER_NAME_SCHEMA
    )


class CarUpdate(SQLModel):
    '''Class for Car update'''
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


@event.listens_for(Manufacturer, 'before_insert')
@event.listens_for(Manufacturer, 'before_update')
def normalize_manufacturer_name(_mapper, _connection, target):
    '''Lowercase Manufacturer name before commiting to database'''
    if target.name and isinstance(target.name, str):
        target.name = target.name.lower().strip()


@event.listens_for(Car, 'before_insert')
@event.listens_for(Car, 'before_update')
def normalize_car_fields(_mapper, _connection, target):
    '''Lowercase Car name and color before commiting to database'''
    if target.name and isinstance(target.name, str):
        target.name = target.name.lower().strip()

    if target.color and isinstance(target.color, str):
        target.color = target.color.lower().strip()
