from fastapi import FastAPI, Depends, status, Path
import models
from db import engine
from routers import auth, books


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# include auth scripts
app.include_router(auth.router)
app.include_router(books.router)

