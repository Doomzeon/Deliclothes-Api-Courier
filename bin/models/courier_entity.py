
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList

Base = declarative_base()

class CourierEntity(Base):
    __tablename__ = 'COURIERS'

    id = Column(Integer, primary_key=True)
    phone= Column(Integer)
    email= Column(String)
    password= Column(String)
    name= Column(String)
    surname= Column(String)
    type_vehicle= Column(String)
    
    

    