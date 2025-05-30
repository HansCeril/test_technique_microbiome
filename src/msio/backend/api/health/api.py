from fastapi import APIRouter

from msio.backend.api.health.endpoints import health

api_router_health = APIRouter()


##############################
#        FRONTEND            #
##############################

api_router_health.include_router(health.router, prefix="/status", tags=["Health Check"])
