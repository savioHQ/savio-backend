from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.id'))
    slider_default = Column(String, default='0.5')
    preferred_tone = Column(String, default='neutral')
    emergency_contact = Column(String, nullable=True)

class Example(Base):
    __tablename__ = 'examples'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tone = Column(String)
    text = Column(Text)

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=True)
    message = Column(Text)
    response = Column(Text)
    tone = Column(String)
    emotion = Column(String)
    safety_flags = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
