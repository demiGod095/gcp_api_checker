from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Job(Base):
    __tablename__ = 'Jobs_jobmodel'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False)
    tries = Column(Integer)
    code = Column(Integer)
    response = Column(Text) # unused
    created_at = Column(DateTime)
    updated_at = Column(DateTime, onupdate=func.now())
