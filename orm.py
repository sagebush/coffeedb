from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Origin(Base):
    __tablename__ = 'origin'
    id = Column('id', INTEGER, primary_key=True)
    refName = Column('ref_name', VARCHAR(128))

class Processing(Base):
    __tablename__ = 'processing'
    id = Column('id', INTEGER, primary_key=True)
    refName = Column('ref_name', VARCHAR(128))
