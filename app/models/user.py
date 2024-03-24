from ..db.session import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, PrimaryKeyConstraint

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)