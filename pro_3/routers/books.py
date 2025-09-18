from fastapi import APIRouter, Depends, status, Path
from db import session_local
from typing import Annotated
from sqlalchemy.orm import Session
from models import Books
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field

router  = APIRouter()

def get_db():
    db_conn = session_local()
    try:
        yield db_conn
    finally:
        db_conn.close()

db_dependency =  Annotated[Session, Depends(get_db)]

class BookRequest(BaseModel):
    title:str = Field(min_length=3)
    rating:int = Field(gt=-1 , lt=6, description="Rating should be between 0 to 6") 

class Book:
    id:int
    title:str
    rating:int
    def __init__(self, id:int, title:str, rating:int) -> None:
        self.id = id
        self.title = title
        self.rating = rating


# Depneds - this is for the dependency 
@router.get("/", )
async def read_all(db: db_dependency):
    return db.query(Books).all()


@router.get("/book/{id}", status_code=status.HTTP_200_OK)
async def read_book(db: db_dependency, id:int = Path(gt=0)):
    book = db.query(Books).filter(Books.id== id).first()
    if book is not None:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.post("/book", status_code=status.HTTP_201_CREATED)
async def create_book(db:db_dependency, book_request:BookRequest):
    book = Books(**book_request.model_dump())
    db.add(book)
    db.commit()

@router.put("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(db:db_dependency, book_request: BookRequest, id: int = Path(gt=0)):

    book = db.query(Books).filter(Books.id ==id ).first()

    if book is None:
        raise HTTPException(status_code=404, detail = "Book not found")
    
    book.title = book_request.title
    book.rating = book_request.rating

    db.add(book)
    db.commit()