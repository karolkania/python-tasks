from typing import List, Optional
from pydantic import BaseModel, Field


class CarBase(BaseModel):
    make: str
    model: str


class CarIn(CarBase):
    pass


class Car(CarBase):
    id: int
    rating: int = None
    votes: int = None

    class Config:
        orm_mode = True


class CarDB(Car):
    votesum: int = None


class CarRateIn(BaseModel):
    id: int
    rating: int = Field(..., gt=0, lt=6)


class VehicleListingModel(BaseModel):
    Make_ID: int
    Make_Name: str
    Model_ID: int
    Model_Name: str


class VehicleListingModelsForMake(BaseModel):
    Count: int
    Message: Optional[str] = None
    SearchCriteria: str
    Results: List[VehicleListingModel]
