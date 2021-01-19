from typing import Optional, List
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx


app = FastAPI()


class Car(BaseModel):
    Make: str
    Model: str


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/cars")
def add_car(car: Car):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{car.Make}?format=json"
    with httpx.Client() as client:
        external_api = client.get(url)
    data = VehicleListingModelsForMake.parse_obj(external_api.json())
    if data.Count > 0:
        foundInVpicDb = False
        for vpicRecord in data.Results:
            if car.Model.lower() == vpicRecord.Model_Name.lower():
                foundInVpicDb = True
                break

        if foundInVpicDb:
            car.Make, car.Model = vpicRecord.Make_Name, vpicRecord.Model_Name
            msg = f"model {car.Model} of make {car.Make} found in vpic"
            return {"msg": msg}
        else:
            msg = f"model '{car.Model}' of make '{car.Make}' does not exist (in vpic)"
            raise HTTPException(status_code=404, detail=msg)
    else:
        msg = f"make '{car.Make}' does not exist (in vpic)"
        raise HTTPException(status_code=404, detail=msg)


# @app.post("/rate")
# def rate_car(car: Car, rate: int = Body(..., ge=1, le=5)):
#     pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
