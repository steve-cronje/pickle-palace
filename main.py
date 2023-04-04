from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import routers.home.controller as home

app = FastAPI()



app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(home.router)


