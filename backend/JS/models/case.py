from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class YearLoss(BaseModel):
    year: int = Field(..., ge=2000, le=2100)  # Validasi tahun relevan SDG data
    tc_loss_ha: float = Field(..., ge=0)  # Hectares >=0

class DriverData(BaseModel):
    driver: str
    losses: List[YearLoss]

class Case(BaseModel):
    country: str
    threshold: int = 30  # Default dari data
    drivers: List[DriverData] = []
    sdg_indicator: Optional[str] = "15.2.1"  # Link ke SDG 15

    @field_validator('drivers')
    @classmethod
    def validate_no_duplicate_years(cls, drivers: List[DriverData]) -> List[DriverData]:
        for driver_data in drivers:
            years = [loss.year for loss in driver_data.losses]
            if len(years) != len(set(years)):
                raise ValueError("Duplicate years in losses for a driver")
            if len(years) == 0:
                raise ValueError("At least 1 loss entry required per driver")
        return drivers