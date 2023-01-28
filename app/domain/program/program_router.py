from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from database import get_db
from models import Program, VCAC
from domain.program import program_schema, program_crud
from domain.vcac.vcac_router import get_current_vcac

router = APIRouter(
    prefix="/program"
)


@router.post("/")
def program_create(
        _program_create: program_schema.ProgramBase,
        db: Session = Depends(get_db),
        current_user: VCAC = Depends(get_current_vcac)
):
    #
    program_crud.create_program(
        db, _program_create, current_user
    )


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def program_update(_program_update: program_schema.ProgramBase,
                 db: Session = Depends(get_db),
                 current_user: VCAC = Depends(get_current_vcac)):
    program_crud.update_program(
        db=db,
        program_update=_program_update,
        vcac=current_user
    )


@router.get("/list", response_model=List[program_schema.ProgramBase])
def program_list(
        db: Session = Depends(get_db),
):
    return program_crud.read_program_list(db)


@router.get("/{title}", response_model=program_schema.ProgramBase)
def program_read(title: str, db: Session = Depends(get_db)):
    return program_crud.read_program(
        db,
        title=title
    )


@router.delete("/{title}", status_code=status.HTTP_204_NO_CONTENT)
def program_delete(title: str,
                 db: Session = Depends(get_db),
                 current_user: VCAC = Depends(get_current_vcac)):
    program_crud.delete_program(
        db=db,
        title=title,
        vcac=current_user
    )

