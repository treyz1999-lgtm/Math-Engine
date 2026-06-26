from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import history_routes
# ROUTERS
from routes.arithmetic_routes import router as arithmetic_router
from routes.trig_routes import router as trig_router
from routes.expression_routes import router as expression_router
from routes.settings_routes import router as settings_router
from routes.geometry_2d_routes import router as geometry_2d_router
from routes.geometry_3d_routes import router as geometry_3d_router
from routes.stats_routes import router as stats_router
from routes.linear_routes import router as linear_router
from routes.plot_routes import router as plot_router
from routes.history_routes import router as history_router

app = FastAPI(
    title="Calculator API",
    version="1.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": (
            "'I'm Your Huckleberry...' "
            "I haven't even seen Tombstone but Doc Holiday had aura in that clip. "
            "A job would be cool too."
        )
    }

# REGISTER ROUTERS
app.include_router(arithmetic_router)
app.include_router(trig_router)
app.include_router(expression_router)
app.include_router(settings_router)
app.include_router(geometry_2d_router)
app.include_router(geometry_3d_router)
app.include_router(stats_router)
app.include_router(linear_router)
app.include_router(plot_router)

app.include_router(history_router)