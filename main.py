from fastapi import FastAPI
from routes.trig_routes import router as trig_router

app = FastAPI(
    title="Calculator API",
    version="1.0"
)


@app.get("/")
def root():
    return {"message": "Calculator API running"}


app.include_router(trig_router)