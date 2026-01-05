from app.models.case import Case, YearLoss, DriverData
from app.db_connection import get_collection
from bson import ObjectId
from typing import List, Dict, Optional
from fastapi import HTTPException

collection = get_collection()

def create_or_append_case(country: str, driver: str, losses: List[Dict]) -> str:
    if not losses:
        raise HTTPException(status_code=422, detail="At least 1 loss entry required")

    # Konversi ke YearLoss, validasi min 1
    loss_objects = [YearLoss(**loss) for loss in losses]  # Expect [{"year": 2021, "tc_loss_ha": 999}, ...]

    # Cari existing
    existing = collection.find_one({"country": country})
    if not existing:
        new_driver = DriverData(driver=driver, losses=loss_objects)
        new_case = Case(country=country, drivers=[new_driver])
        result = collection.insert_one(new_case.model_dump())
        return str(result.inserted_id)

    # Check driver
    driver_index = next((i for i, d in enumerate(existing['drivers']) if d['driver'] == driver), None)
    if driver_index is None:
        new_driver = DriverData(driver=driver, losses=loss_objects).model_dump()
        collection.update_one({"_id": existing['_id']}, {"$push": {"drivers": new_driver}})
        return str(existing['_id'])

    # Check duplicate years
    existing_years = {loss['year'] for loss in existing['drivers'][driver_index]['losses']}
    for loss in loss_objects:
        if loss.year in existing_years:
            raise HTTPException(status_code=409, detail=f"Duplicate year {loss.year} for {country}/{driver}")

    # Append
    collection.update_one(
        {"_id": existing['_id'], "drivers.driver": driver},
        {"$addToSet": {"drivers.$.losses": {"$each": [l.model_dump() for l in loss_objects]}}}  # $addToSet cegah duplikat
    )
    return str(existing['_id'])

# Fungsi lama tetap untuk full create jika perlu
def create_case(case: Case) -> str:
    # Check duplikat di level model
    return str(collection.insert_one(case.model_dump()).inserted_id)

def read_cases(country: Optional[str] = None, driver: Optional[str] = None, year: Optional[int] = None, page: int = 1, limit: int = 10) -> List[Dict]:
    query = {}
    if country: query["country"] = {"$regex": country, "$options": "i"}  # Insensitive
    if driver: query["drivers.driver"] = {"$regex": driver, "$options": "i"}
    if year: query["drivers.losses.year"] = year

    cursor = collection.find(query, {"_id": 0}).sort([("drivers.losses.year", -1)]).skip((page - 1) * limit).limit(limit)
    return list(cursor)

def update_case(country: str, driver: str, year: int, new_data: Dict) -> bool:
    if not new_data:
        raise HTTPException(status_code=400, detail="No data to update")

    # Check existence
    existing = collection.find_one({
        "country": country,
        "drivers": {"$elemMatch": {"driver": driver, "losses.year": year}}
    })
    if not existing:
        raise HTTPException(status_code=404, detail=f"Data not found for {country}/{driver}/{year}")

    # Update specific loss
    driver_index = next(i for i, d in enumerate(existing['drivers']) if d['driver'] == driver)
    loss_index = next(i for i, l in enumerate(existing['drivers'][driver_index]['losses']) if l['year'] == year)

    update_path = f"drivers.{driver_index}.losses.{loss_index}"
    result = collection.update_one({"_id": existing['_id']}, {"$set": {f"{update_path}.{k}": v for k, v in new_data.items()}})
    return result.modified_count > 0

def delete_case(country: str, driver: Optional[str] = None, year: Optional[int] = None) -> bool:
    if not driver:
        # Delete entire country
        result = collection.delete_one({"country": country})
        return result.deleted_count > 0

    if not year:
        # Delete entire driver
        result = collection.update_one({"country": country}, {"$pull": {"drivers": {"driver": driver}}})
        return result.modified_count > 0

    # Delete specific year
    result = collection.update_one(
        {"country": country, "drivers.driver": driver},
        {"$pull": {"drivers.$.losses": {"year": year}}}
    )
    return result.modified_count > 0