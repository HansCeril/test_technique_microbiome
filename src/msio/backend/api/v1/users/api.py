from fastapi import APIRouter

from msio.backend.api.v1.users.endpoints import users

api_router_users = APIRouter()


##############################
#        FRONTEND            #
##############################

api_router_users.include_router(users.router, prefix="/users", tags=["USER API"])
