from db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = "Users"
    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    hash_password = Column(String)
    is_active = Column(Boolean, default=True)



class Books(Base):
    __tablename__ = "Books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    rating = Column(Integer)
    added_by =Column(Integer, ForeignKey("Users.uid"))




