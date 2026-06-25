from fastapi import FastAPI
from routes.trig_routes import router as trig_router
from routes.arithmetic_routes import router as arithmetic_router

app = FastAPI(
    title="Calculator API",
    version="1.0"
)


@app.get("/")
def root():
    return {"message": "'I'm Your Huckleberry'... I haven't even seen Tombstone but Doc Holiday had aura in that clip... a job would be cool too"}


app.include_router(trig_router)
app.include_router(arithmetic_router)
