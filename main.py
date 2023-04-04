from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import routers.home.controller as home
import routers.pickle.controller as pickle

app = FastAPI()



app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(home.router)
app.include_router(pickle.router)


