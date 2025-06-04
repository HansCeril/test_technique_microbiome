from fastapi import APIRouter

from msio.backend.api.v1.metabolites.endpoints import metabolites

api_router_metabolites = APIRouter()


##############################
#        FRONTEND            #
##############################

api_router_metabolites.include_router(
    metabolites.router, prefix="/metabolites", tags=["metabolites API"]
)
