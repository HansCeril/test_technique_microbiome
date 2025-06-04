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
    """
    Create a new metabolite in the database.

    This endpoint allows an authenticated user to submit a new
    metabolite entry.

    Args:
        payload (MetaboliteCreate): The data of the metabolite to be created.
        db (AsyncSession): The asynchronous database session.
        current_user (User): The currently authenticated user, extracted from
        the JWT token.

    Returns:
        MetaboliteRead: The newly created metabolite with its generated ID
        and associated metadata.
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
    Retrieve a single metabolite by its ID.

    This endpoint returns the metabolite stored in the database.
    It requires the user to be authenticated.

    Args:
        metabolite_id (int): The ID of the metabolite to retrieve.
        db (AsyncSession): The asynchronous database session.
        current_user (User): The currently authenticated user,
            extracted from the JWT token.

    Raises:
        HTTPException: Returns 404 if the metabolite is not found.
    """
    result = await db.execute(select(Metabolite).where(Metabolite.id == metabolite_id))
    metabolite = result.scalar_one_or_none()
    if not metabolite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Metabolite not found"
        )
    return metabolite


@router.put("/{metabolite_id}", response_model=MetaboliteRead)
async def update_metabolite(
    metabolite_id: int,
    payload: MetaboliteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing metabolite by its ID.

    This endpoint allows an authenticated user to update a metabolite.
    The metabolite is identified by its unique ID, and all fields
    provided in the payload will overwrite the current values.

    Args:
        metabolite_id (int): The ID of the metabolite to update.
        payload (MetaboliteCreate): The new data for the metabolite.
        db (AsyncSession): The asynchronous database session.
        current_user (User): The currently authenticated user.

    Raises:
        HTTPException: Returns 404 if the metabolite is not found.

    Returns:
        MetaboliteRead: The updated metabolite data.
    """
    result = await db.execute(select(Metabolite).where(Metabolite.id == metabolite_id))
    metabolite = result.scalar_one_or_none()
    if not metabolite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Metabolite not found"
        )

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
    Delete an existing metabolite by its ID.

    This endpoint allows an authenticated user to delete a metabolite
    from the database.
    The metabolite is identified by its unique ID. If no metabolite is
    found with the provided ID, a 404 error is returned.

    Args:
        metabolite_id (int): The ID of the metabolite to delete.
        db (AsyncSession): The asynchronous database session.
        current_user (User): The currently authenticated user.

    Raises:
        HTTPException: Returns 404 if the metabolite is not found.

    Returns:
        None: Successful deletion returns a 204 No Content status.
    """
    result = await db.execute(select(Metabolite).where(Metabolite.id == metabolite_id))
    metabolite = result.scalar_one_or_none()
    if not metabolite:
        raise HTTPException(status_code=404, detail="Metabolite not found")

    await db.delete(metabolite)
    await db.commit()
