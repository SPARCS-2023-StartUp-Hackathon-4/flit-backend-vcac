import datetime

from sqlalchemy import Column, Integer, String,\
    Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from typing import Tuple

from database import Base


class VCAC(Base):
    __tablename__ = "vcac"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Program(Base):
    __tablename__ = "program"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)      # 지원 사업
    url = Column(String, nullable=False)
    category = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    apply_period = Column(String, nullable=False)
    apply_method = Column(String, nullable=False)
    content = Column(String, nullable=False)
    inquiries = Column(String, nullable=False)
    age = Column(String, nullable=False)

    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=False)

    vcac_id = Column(Integer, ForeignKey("vcac.id"), nullable=True)
    vcac = relationship("VCAC", backref="program_vcac")

