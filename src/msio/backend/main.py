import uvicorn
from fastapi import FastAPI
from src.msio.backend.core.config import config

from msio.backend.log import configure_logging
from msio.backend.api.health.api import api_router_health
from fastapi.middleware.cors import CORSMiddleware


VERSION = config.VERSION
VERSION_PREFIX = f"/api/{VERSION}"

app = FastAPI(
    title="test_misio",
    description="Technical test misio",
    version=VERSION,
    contact={
        "name": "Hans",
        "email": "anselmeceril@gmail.com",
    },
    openapi_url=f"{VERSION_PREFIX}/openapi.json",
    docs_url=f"{VERSION_PREFIX}/docs",
    redoc_url=f"{VERSION_PREFIX}/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router_health)


if __name__ == "__main__":
    configure_logging()
    uvicorn.run(app, log_config=None)
