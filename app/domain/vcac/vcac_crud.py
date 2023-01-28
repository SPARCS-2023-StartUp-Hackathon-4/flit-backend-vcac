from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.vcac.vcac_schema import VcacCreate
from models import VCAC


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_vcac(db: Session, vcac_create: VcacCreate):
    db_user = VCAC(
        username=vcac_create.username,
        password=pwd_context.hash(vcac_create.password1),
        email=vcac_create.email
    )
    db.add(db_user)
    db.commit()


def get_vcac(db: Session, username: str):
    return db.query(VCAC).filter(VCAC.username == username).first()


def delete_vcac(db: Session, username: str):
    db_user = db.query(VCAC).filter(
        VCAC.username == username
    ).first()
    db.delete(db_user)
    db.commit()


def get_existing_vcac(db: Session, vcac_create: VcacCreate):
    return db.query(VCAC).filter(
        (VCAC.username == vcac_create.username) |
        (VCAC.email == vcac_create.email)
    ).first()
