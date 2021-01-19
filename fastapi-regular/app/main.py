from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException  # Body
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
    return crud.get_cars(db=db)


@app.post("/cars", response_model=schemas.Car)
def add_car(car: schemas.CarIn, db: Session = Depends(get_db)):
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


# @app.post("/rate")
# def rate_car(car: Car, rate: int = Body(..., ge=1, le=5)):
#     pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
