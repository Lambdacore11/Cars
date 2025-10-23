from decimal import Decimal
from sqlmodel import SQLModel, CheckConstraint, Field


class CarBase(SQLModel):
    name:str = Field(index=True, max_length=50, regex=r'^[a-zA-Z0-9\-]+$')
    color:str = Field(index=True, max_length=50, regex=r'^[a-zA-Z\-]+$')
    price:Decimal = Field(default=0, max_digits=11, decimal_places=2, ge=Decimal('0'))

class Car(CarBase, table=True):
    __tablename__ = 'cars'
    id:int|None = Field(default=None, primary_key=True)
    __table_args__ = (
        CheckConstraint("name ~ '^[a-zA-Z0-9\\-]+$'", name='check_name_regex'),
        CheckConstraint("color ~ '^[a-zA-Z\\-]+$'", name='check_color_regex'),
        CheckConstraint('price >= 0', name='check_price_positive'),
    )

class CarPublic(CarBase):
    id:int

class CarCreate(CarBase):
    pass

class CarUpdate(SQLModel):
    name:str|None = Field(default=None, max_length=50, regex=r'^[a-zA-Z0-9\-]+$')
    color:str|None = Field(default=None, max_length=50, regex=r'^[a-zA-Z\-]+$')
    price:Decimal|None = Field(default=None, max_digits=11, decimal_places=2, ge=Decimal('0'))
