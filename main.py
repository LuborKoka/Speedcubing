from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.solutions_router import router as solutions_router
from app.routers.scramble_router import router as scramble_router
from app.routers.pages_router import router as view_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/view/static"), name="static")


app.include_router(solutions_router, tags=['solutions'])
app.include_router(scramble_router, tags=['scramble'])


# this one needs to go last
app.include_router(view_router)


    