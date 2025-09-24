from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# Your existing User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    access_token = Column(Text)
    refresh_token = Column(Text)

    # Relationship to tasks (one-to-many)
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")


# New Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    deadline = Column(DateTime, default=datetime.utcnow)   # deadline stored as datetime
    importance = Column(Integer, default=1)                # can store priority levels (1=low, 5=high)
    notes = Column(Text)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to User
    user = relationship("User", back_populates="tasks")
