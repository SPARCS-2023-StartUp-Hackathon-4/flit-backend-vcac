from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.vcac import vcac_crud, vcac_schema
from domain.vcac.vcac_crud import pwd_context
from commmon.config import SECRET_KEY


ACCESS_TOKEN_EXPIRE_MINUTES = 60*24
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/vcac/login")


router = APIRouter(
    prefix="/vcac"
)


@router.post("/", status_code=status.HTTP_200_OK)
def user_create(_vcac_create: vcac_schema.VcacCreate,
                db: Session = Depends(get_db)):
    user_exists = bool(
        vcac_crud.get_existing_vcac(db, vcac_create=_vcac_create)
    )

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Existing vcac')
    vcac_crud.create_vcac(db=db,
                          vcac_create=_vcac_create)


@router.get("/", response_model=vcac_schema.VcacGet)
def get_current(token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):

    current_user = get_current_vcac(token, db)
    return current_user


@router.post("/login", response_model=vcac_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    #
    vcac = vcac_crud.get_vcac(db, form_data.username)
    if not vcac or not pwd_context.verify(form_data.password, vcac.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect Username or PW',
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Make Access Token
    data = {
        "sub": vcac.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(
        data, SECRET_KEY, algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": vcac.username
    }


@router.post("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def vcac_delete(username: str,
                token: str = Depends(oauth2_scheme),
                db: Session = Depends(get_db)):
    current_user = get_current_vcac(token, db)
    if current_user.username == username:
        vcac_crud.delete_vcac(db, username)

    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Incorrect Username')


def get_current_vcac(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    else:
        user = vcac_crud.get_vcac(db, username=username)
        if user is None:
            raise credentials_exception
        return user
