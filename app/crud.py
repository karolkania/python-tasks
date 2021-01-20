from sqlalchemy.orm import Session

from . import models, schemas


def get_car_by_id(db: Session, car_id: int):
    return db.query(models.Car).filter(models.Car.id == car_id).first()


def get_car_by_model(db: Session, car_model: str):
    return db.query(models.Car).filter(models.Car.model == car_model).first()


def get_cars(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Car).offset(skip).limit(limit).all()


def add_car(db: Session, car: schemas.CarIn):
    db_car = models.Car(make=car.make, model=car.model)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def rate_car(db: Session, car: schemas.CarDB):
    db.query(models.Car).filter(models.Car.id == car.id).update(
        {
            models.Car.rating: car.rating,
            models.Car.votes: car.votes,
            models.Car.votesum: car.votesum,
        }
    )
    db.commit()
    return db.query(models.Car).filter(models.Car.id == car.id).first()


def get_popular(db: Session):
    return db.query(models.Car).filter(models.Car.votes != None).order_by(models.Car.votes.desc()).all()
