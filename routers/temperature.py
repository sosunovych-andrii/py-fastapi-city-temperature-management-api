from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_db
from schemas.temparature import TemperatureReadSchema
from services.temparature import (
    update_temperatures as update_temperatures_service,
    get_temperatures as get_temperatures_service,
    get_temperature as get_temperature_service
)

temperature_router = APIRouter(prefix="/temperatures")


@temperature_router.post("/update/")
async def update_temperatures_endpoint(db: AsyncSession = Depends(get_db)):
    cities_updated = await update_temperatures_service(db)
    return {
        "status": "Temperatures updated successfully",
        "cities_updated": cities_updated
    }

@temperature_router.get(
    path="/",
    response_model=list[TemperatureReadSchema]
)
async def get_temperatures(db: AsyncSession = Depends(get_db)):
    return await get_temperatures_service(db)


@temperature_router.get(
    path="/{temp_id}/",
    response_model=TemperatureReadSchema
)
async def get_temperature(
        temp_id,
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
):
    return await get_temperature_service(temp_id, city_id, db)
