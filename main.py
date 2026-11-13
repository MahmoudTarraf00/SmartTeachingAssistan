from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import database
from routes import auth, pages

database.init_db()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pages.router)
app.include_router(auth.router)
