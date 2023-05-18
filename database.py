import datetime
from sqlalchemy import MetaData, Table, create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
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

class Estate(Base):
    __tablename__ = "estates"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    address = Column(String)
    tenants = relationship("Tenant", back_populates="estate",cascade="all, delete")
    notifications = relationship("Notification", back_populates="estate",cascade="all, delete")


class Notification(Base):
    __tablename__ = "notifications"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    message = Column(String, index=True)
    created_at = Column(DateTime,index=True)
    estate_id = Column(Integer, ForeignKey("estates.id"), index=True)
    estate = relationship("Estate", back_populates="notifications")
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", back_populates="notifications")

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
    tenants = relationship("Tenant", back_populates="user", cascade="all, delete")
    notifications = relationship("Notification", back_populates="user",cascade="all, delete")
    role_id = Column(Integer, ForeignKey("user_role.id"), index=True)
    user_role = relationship("UserRole", back_populates="users")

class UserRole(Base):
    __tablename__ = "user_role"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    users = relationship("User", back_populates="user_role")

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    description = Column(String)
    status = Column(String)
    type_id = Column(Integer, ForeignKey("support_ticket_types.id"),index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    created_at = Column(DateTime,index=True)
    update_date = Column(DateTime, index=True, default=None)
    ticket_type = relationship("SupportTicketType", back_populates="tickets")
    tenant = relationship("Tenant", back_populates="tickets")


class SupportTicketType(Base):
    __tablename__ = "support_ticket_types"
    metadata = metadata

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    create_date = Column(DateTime, index=True)
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
    unitNr = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    create_date = Column(DateTime, index=True)
    update_date = Column(DateTime, index=True, default=None)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", back_populates="tenants")
    visitors = relationship("Visitor", back_populates="tenant", cascade="all, delete")
    tickets = relationship("SupportTicket", back_populates="tenant", cascade="all, delete")
    chat_messagges = relationship("ChatMessage", back_populates="tenant", cascade="all, delete")
    estate_id = Column(Integer, ForeignKey("estates.id"), index=True)
    estate = relationship("Estate", back_populates="tenants")


class Visitor(Base):
    __tablename__ = "visitors"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String, index=True)
    name = Column(String, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    car_id = Column(Integer, index=True)
    create_date = Column(DateTime, index=True)
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
    
class ChatMessage(Base):
    __tablename__ = "chat_messagges"
    metadata = metadata
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(String, index=True)
    username = Column(String, index=True)
    sender = Column(String, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    create_date = Column(DateTime, index=True)
    tenant = relationship("Tenant", back_populates="chat_messagges")
    
Base.metadata.create_all(engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()