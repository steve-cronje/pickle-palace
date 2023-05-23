from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import routers.home.controller as home
import routers.pickle.controller as pickle
import routers.games.controller as games
import routers.users.controller as users


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(home.router)
app.include_router(pickle.router)
app.include_router(games.router)
app.include_router(users.router)



