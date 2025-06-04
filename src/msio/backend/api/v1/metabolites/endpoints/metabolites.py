from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from msio.backend.database.models import Metabolite, User
from msio.backend.core.auth import get_current_user
from msio.backend.database.session import get_db
from src.msio.backend.database.schemas import MetaboliteCreate, MetaboliteRead


router = APIRouter()


@router.get("/", response_model=list[MetaboliteRead])
async def list_metabolites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve all metabolites from the database.

    Args:
        db (AsyncSession): SQLAlchemy asynchronous session,
        provided by FastAPI dependency injection.

    Returns:
        list[MetaboliteRead]: List of metabolite records.
    """
    result = await db.execute(select(Metabolite))
    return result.scalars().all()


@router.post("/", response_model=MetaboliteRead, status_code=status.HTTP_201_CREATED)
async def create_metabolite(
    payload: MetaboliteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """_summary_

    Args:
        payload (MetaboliteCreate): _description_
        db (AsyncSession, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    metabolite = Metabolite(**payload.model_dump(), uploader_id=current_user.id)
    db.add(metabolite)
    await db.commit()
    await db.refresh(metabolite)
    return metabolite


@router.get("/{metabolite_id}", response_model=MetaboliteRead)
async def get_metabolite(
    metabolite_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a single metabolite by ID.
    """
    result = await db.execute(select(Metabolite).where(Metabolite.id == metabolite_id))
    metabolite = result.scalar_one_or_none()
    if not metabolite:
        raise HTTPException(status_code=404, detail="Metabolite not found")
    return metabolite


@router.put("/{metabolite_id}", response_model=MetaboliteRead)
async def update_metabolite(
    metabolite_id: int,
    payload: MetaboliteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a metabolite's data.
    """
    result = await db.execute(select(Metabolite).where(Metabolite.id == metabolite_id))
    metabolite = result.scalar_one_or_none()
    if not metabolite:
        raise HTTPException(status_code=404, detail="Metabolite not found")

    for key, value in payload.model_dump().items():
        setattr(metabolite, key, value)
    await db.commit()
    await db.refresh(metabolite)
    return metabolite


@router.delete("/{metabolite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metabolite(
    metabolite_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a metabolite by ID.
    """
    result = await db.execute(select(Metabolite).where(Metabolite.id == metabolite_id))
    metabolite = result.scalar_one_or_none()
    if not metabolite:
        raise HTTPException(status_code=404, detail="Metabolite not found")

    await db.delete(metabolite)
    await db.commit()
