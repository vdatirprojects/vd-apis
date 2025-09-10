from fastapi import FastAPI, Path, Query, HTTPException
from starlette import status
from pydantic import BaseModel, Field
from typing import Optional
app = FastAPI()




class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Id is not required while creating book", default=None)
    title:str = Field(min_length=5, max_length=15)
    rating:int = Field(gt=-1 , lt=6, description="Rating should be between 0 to 6") 

    model_config ={

        "json_schema_extra":
        {
            "example":{
                "title":"A new book",
                "rating": 5
            }
        }
    }

class Book:
    id:int
    title:str
    rating:int
    def __init__(self, id:int, title:str, rating:int) -> None:
        self.id = id
        self.title = title
        self.rating = rating


BOOKS =[Book(1, "DS Book", 5),
        Book(2, "DE Book", 5)]


def get_auto_book_id(book:Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id +1
    else:
        book.id =1
    return book


@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(get_auto_book_id(new_book))

# path parameter
@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def get_single_book(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
        

# query parameter
@app.get("/book", status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating:int= Query(gt=-1, lt=6)):
    books_rating =[]
    for book in BOOKS:
        if book.rating == rating:
            books_rating.append(book)
    return books_rating

@app.put("/book/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(update_book:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == update_book.id:
            BOOKS[i] = update_book            
        else:
            raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/book",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int=Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
        else:
            raise HTTPException(status_code=404, detail="Book not found")