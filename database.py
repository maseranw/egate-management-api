import datetime
from sqlalchemy import MetaData, create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


database_url = os.environ.get('DATABASE_URL')


SQLALCHEMY_DATABASE_URL = database_url

metadata = MetaData()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    phone = Column(String, index=True)
    password = Column(String)
    create_date = Column(DateTime, index=True)
    update_date = Column(DateTime, index=True)
    tenants = relationship("Tenant", back_populates="user")

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    type_id = Column(Integer, ForeignKey("support_ticket_types.id"),index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now())
    update_date = Column(DateTime, index=True, default=None)
    ticket_type = relationship("SupportTicketType", back_populates="tickets")
    tenant = relationship("Tenant", back_populates="tickets")


class SupportTicketType(Base):
    __tablename__ = "support_ticket_types"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    create_date = Column(DateTime, index=True, default=datetime.datetime.now())
    update_date = Column(DateTime, index=True, default=None)
    tickets = relationship("SupportTicket", back_populates="ticket_type")
    
    
class Tenant(Base):
    __tablename__ = "tenants"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    create_date = Column(DateTime, index=True, default=datetime.datetime.now())
    update_date = Column(DateTime, index=True, default=None)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", back_populates="tenants")
    visitors = relationship("Visitor", back_populates="tenant")
    tickets = relationship("SupportTicket", back_populates="tenant")

class Visitor(Base):
    __tablename__ = "visitors"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String, index=True, unique=True, )
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    car_id = Column(Integer, index=True)
    create_date = Column(DateTime, index=True, default=datetime.datetime.now())
    update_date = Column(DateTime, index=True, default=None)
    check_in_time = Column(DateTime, index=True, default=None)
    check_out_time = Column(DateTime, index=True, default=None)
    tenant = relationship("Tenant", back_populates="visitors")
    access_codes = relationship("AccessCode", back_populates="visitor")

    
class AccessCode(Base):
    __tablename__ = "access_codes"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"), index=True)
    code = Column(Numeric, unique=True, index=True)
    create_date = Column(DateTime, index=True)
    update_date = Column(DateTime, index=True)
    expiry_date = Column(DateTime, index=True)
    visitor = relationship("Visitor", back_populates="access_codes")


class Car(Base):
    __tablename__ = "cars"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(String, index=True)
    create_date = Column(DateTime, index=True)
    update_date = Column(DateTime, index=True)
    

Base.metadata.create_all(engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()