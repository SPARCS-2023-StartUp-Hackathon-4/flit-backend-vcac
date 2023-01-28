from sqlalchemy.orm import Session
from datetime import datetime

from domain.program.program_schema import ProgramBase
from models import Program, VCAC


def create_program(db: Session,
                   program_create: ProgramBase,
                   vcac: VCAC):
    db_program = Program(
        title=program_create.title,
        url=program_create.url,
        category=program_create.category,
        organization=program_create.organization,
        subject=program_create.subject,
        apply_period=program_create.apply_period,
        apply_method=program_create.apply_method,
        content=program_create.content,
        inquiries=program_create.inquiries,
        age=program_create.age,
        create_date=datetime.now(),
        update_date=datetime.now(),
        vcac=vcac
    )
    db.add(db_program)
    db.commit()


def read_program(db: Session,
                 title: str):
    program = db.query(Program).filter(Program.title == title).first()
    return program


def read_program_list(db: Session):
    program = db.query(Program).all()
    return program


def update_program(db: Session,
                   program_update: ProgramBase,
                   vcac: VCAC):
    db_program = db.query(Program).filter(
        (Program.title == program_update.title) & (Program.vcac_id == vcac.id)).first()

    db_program.title = program_update.title
    db_program.url = program_update.url
    db_program.category = program_update.category
    db_program.organization = program_update.organization
    db_program.subject = program_update.subject
    db_program.apply_period = program_update.apply_period
    db_program.apply_method = program_update.apply_method
    db_program.content = program_update.content
    db_program.inquiries = program_update.inquiries
    db_program.age = program_update.age
    db_program.update_date = datetime.now()

    db.add(db_program)

    db.commit()


def delete_program(db: Session,
                   title: str,
                   vcac: VCAC):
    db_program = db.query(Program).filter(
        (Program.title == title) & (Program.vcac_id == vcac.id)).first()

    db.delete(db_program)

    db.commit()
