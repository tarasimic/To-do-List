from ..db.session import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, PrimaryKeyConstraint, Date
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User", back_populates='tasks')

    def __init__(self, name: str, description: str=None, due_date: Date=None):
        self.name = name
        self.description = description
        self.due_date = due_date