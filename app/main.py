from typing import Optional, List
from fastapi import Body, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

import uvicorn
import httpx

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/cars", response_model=List[schemas.Car])
def get_cars(db: Session = Depends(get_db)):
    """
    GET /cars
    - Should fetch list of all cars already present in application database with their current average rate
    """
    return crud.get_cars(db=db)


@app.post("/cars", response_model=schemas.Car)
def add_car(car: schemas.CarIn, db: Session = Depends(get_db)):
    """
    POST /cars
    - Request body should contain car make and model name
    - Based on this data, its existence should be checked here https://vpic.nhtsa.dot.gov/api/
    - If the car doesn't exist - return an error
    - If the car exists - it should be saved in the database
    """
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{car.make}?format=json"
    with httpx.Client() as client:
        external_api = client.get(url)
    data = schemas.VehicleListingModelsForMake.parse_obj(external_api.json())
    if data.Count > 0:
        foundInVpicDb = False
        for vpicRecord in data.Results:
            if car.model.lower() == vpicRecord.Model_Name.lower():
                foundInVpicDb = True
                break

        if foundInVpicDb:
            car.make, car.model = vpicRecord.Make_Name, vpicRecord.Model_Name
            db_car = crud.get_car_by_model(db=db, car_model=car.model)
            if db_car:
                raise HTTPException(status_code=400, detail="Car already saved in db")
            return crud.add_car(db=db, car=car)

        else:
            msg = f"model '{car.model}' of make '{car.make}' does not exist (in vpic)"
            raise HTTPException(status_code=404, detail=msg)
    else:
        msg = f"make '{car.make}' does not exist (in vpic)"
        raise HTTPException(status_code=404, detail=msg)


@app.post("/rate", response_model=schemas.Car)
def rate_car(car_rate_in: schemas.CarRateIn, db: Session = Depends(get_db)):
    """
    POST /rate
    - Add a rate for a car from 1 to 5
    """
    car = crud.get_car_by_id(db=db, car_id=car_rate_in.id)
    if car is None:
        msg = f"the car id: '{car_rate_in.id}' was not found"
        raise HTTPException(status_code=404, detail=msg)

    if car.votes is None:
        car.votes = 1
    else:
        car.votes += 1

    if car.votesum is None:
        car.votesum = car_rate_in.rating
    else:
        car.votesum = car.votesum + car_rate_in.rating

    if car.rating is None:
        car.rating = car_rate_in.rating
    else:
        car.rating = car.votesum / car.votes
    return crud.rate_car(db=db, car=car)


@app.get("/popular", response_model=List[schemas.Car])
def get_popular(db: Session = Depends(get_db)):
    """
    GET /popular
    - Should return top cars already present in the database ranking based on number of rates (not average rate values, it's important!)
    """
    return crud.get_popular(db=db)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
