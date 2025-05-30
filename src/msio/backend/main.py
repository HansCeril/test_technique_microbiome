import uvicorn
from fastapi import FastAPI

from msio.backend.log import configure_logging
from msio.backend.api.health.api import api_router_health


app = FastAPI()
app.include_router(api_router_health)


if __name__ == "__main__":
    configure_logging()
    uvicorn.run(app, log_config=None)
