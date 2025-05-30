from fastapi import APIRouter, status

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {"status": "ok"}
