from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from ..database import SessionDep
from ..models import Manufacturer, ManufacturerPublic, ManufacturerCreate, ManufacturerUpdate


manufacturer_router = APIRouter(prefix='/manufacturers', tags=['manufacturers'])


@manufacturer_router.post(
    '/',
    response_model=ManufacturerPublic,
    status_code=status.HTTP_201_CREATED
)
async def create_manufacturer(
    session: SessionDep,
    new_manufacturer: ManufacturerCreate
):
    manufacturer = Manufacturer.model_validate(new_manufacturer)
    session.add(manufacturer)
    await session.commit()

    return manufacturer


@manufacturer_router.get(
    '/{manufacturer_id}',
    response_model=ManufacturerPublic,
    status_code=status.HTTP_200_OK
)
async def read_manufacturer(
    session: SessionDep,
    manufacturer_id: int
):
    result = await session.execute(
        select(Manufacturer)
        .where(Manufacturer.id == manufacturer_id)
    )

    manufacturer = result.scalars().first()

    if manufacturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Manufacturer not found'
        )

    return manufacturer


@manufacturer_router.get(
    '/',
    response_model=list[ManufacturerPublic],
    status_code=status.HTTP_200_OK
)
async def read_manufacturers(
    session: SessionDep,
):
    result = await session.execute(
        select(Manufacturer)
    )

    manufacturers = result.scalars().all()

    return manufacturers


@manufacturer_router.put(
    '/{manufacturer_id}',
    response_model=ManufacturerPublic,
    status_code=status.HTTP_200_OK
)
async def update_manufacturer(
    session: SessionDep,
    manufacturer_id: int,
    new_manufacturer_data: ManufacturerUpdate
):
    result = await session.execute(
        select(Manufacturer)
        .where(Manufacturer.id == manufacturer_id)
    )

    manufacturer = result.scalars().first()

    if manufacturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Manufacturer not found'
        )

    manufacturer.sqlmodel_update(
        new_manufacturer_data.model_dump(exclude_unset=True)
    )

    session.add(manufacturer)
    await session.commit()

    return manufacturer


@manufacturer_router.delete(
    '/{manufacturer_id}',
    status_code=status.HTTP_200_OK
)
async def delete_manufacturer(
    session: SessionDep,
    manufacturer_id: int
):
    result = await session.execute(
        select(Manufacturer)
        .where(Manufacturer.id == manufacturer_id)
    )

    manufacturer = result.scalars().first()

    if manufacturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Manufacturer not found'
        )

    await session.delete(manufacturer)
    await session.commit()

    return {'message' : 'deleted'}
