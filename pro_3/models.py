from db import Base
from sqlalchemy import Column, Integer, String

class Books(Base):
    __tablename__ = "Books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    rating = Column(Integer)



