from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy import select
from ..database import SessionDep
from ..models import Car, CarPublic, CarCreate, CarUpdate, Manufacturer
from ..schemas import NAME_WITH_DIGITS,NAME_WITHOUT_DIGITS


cars_router = APIRouter(prefix='/cars', tags=['cars'])

@cars_router.post(
    '',
    response_model=CarPublic,
    status_code=status.HTTP_201_CREATED
)
async def create_car(
    session: SessionDep,
    new_car: CarCreate
):
    input_manufacturer_name = new_car.manufacturer_name.lower()
    manufacturer_result = await session.execute(
        select(Manufacturer)
        .where(Manufacturer.name == input_manufacturer_name)
    )
    manufacturer = manufacturer_result.scalars().first()
    car_data = new_car.model_dump(exclude={'manufacturer_name'})

    if manufacturer:
        car = Car(**car_data, manufacturer_id=manufacturer.id)
    else:
        new_manufacturer = Manufacturer(name=input_manufacturer_name)
        session.add(new_manufacturer)
        await session.flush()
        car = Car(**car_data, manufacturer_id=new_manufacturer.id)

    session.add(car)
    await session.commit()

    return CarPublic.model_validate(
        {**car.model_dump(), 'manufacturer_name': input_manufacturer_name}
    )

@cars_router.get(
    '/{car_id}',
    response_model=CarPublic,
    status_code=status.HTTP_200_OK
)
async def read_car(
    session: SessionDep,
    car_id: int
):
    result = await session.execute(
        select(Car, Manufacturer.name)
        .join(Manufacturer)
        .where(Car.id == car_id)
    )

    row = result.first()

    if not row:
        raise HTTPException(status_code=404, detail='Car not found')

    car, manufacturer_name = row

    return CarPublic.model_validate(
        {**car.model_dump(), 'manufacturer_name': manufacturer_name}
    )

@cars_router.get(
    '',
    response_model=list[CarPublic],
    status_code=status.HTTP_200_OK
)
async def read_cars(
    session: SessionDep,
    name: Annotated[str | None, Query(max_length=50, pattern=NAME_WITH_DIGITS)] = None,
    color: Annotated[str | None, Query(max_length=50, pattern=NAME_WITHOUT_DIGITS)] = None,
    manufacturer: Annotated[str | None, Query(max_length=50, pattern=NAME_WITHOUT_DIGITS)] = None
):
    query = select(Car, Manufacturer.name).join(Manufacturer)

    if name:
        query = query.where(Car.name == name.lower())

    if color:
        query = query.where(Car.color == color.lower())

    if manufacturer:
        query = query.where(Manufacturer.name == manufacturer.lower())

    result = await session.execute(query)
    rows = result.all()

    return [
        CarPublic.model_validate(
            {**car.model_dump(), 'manufacturer_name': manufacturer_name}
        )
        for car, manufacturer_name in rows
    ]

@cars_router.put(
    '/{car_id}',
    response_model=CarPublic,
    status_code=status.HTTP_200_OK
)
async def update_car(
    session: SessionDep,
    car_id: int,
    new_car_data: CarUpdate
):
    car_result = await session.execute(
        select(Car)
        .where(Car.id == car_id)
    )

    car = car_result.scalars().first()

    if not car:
        raise HTTPException(status_code=404, detail='Car not found')

    update_data = new_car_data.model_dump(exclude_unset=True)
    manufacturer_name = update_data.pop('manufacturer_name', None)

    if manufacturer_name is not None:
        manufacturer_result = await session.execute(
            select(Manufacturer)
            .where(Manufacturer.name == manufacturer_name)
        )

        manufacturer = manufacturer_result.scalars().first()

        if manufacturer:
            car.manufacturer_id = manufacturer.id
        else:
            new_manufacturer = Manufacturer(name=manufacturer_name)
            session.add(new_manufacturer)
            await session.flush()
            car.manufacturer_id = new_manufacturer.id

    if update_data:
        car.sqlmodel_update(update_data)

    if manufacturer_name is None:
        manufacturer_name_result = await session.execute(
            select(Manufacturer.name)
            .where(Manufacturer.id == car.manufacturer_id)
        )
        manufacturer_name = manufacturer_name_result.scalars().first()

    session.add(car)
    await session.commit()

    return CarPublic.model_validate(
        {**car.model_dump(), 'manufacturer_name': manufacturer_name}
    )

@cars_router.delete(
    '/{car_id}',
    status_code=status.HTTP_200_OK
)
async def delete_car(
    session: SessionDep,
    car_id: int
):
    result = await session.execute(
        select(Car)
        .where(Car.id == car_id)
    )

    car = result.scalars().first()

    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Car not found'
        )

    await session.delete(car)
    await session.commit()

    return {'message' : 'deleted'}
