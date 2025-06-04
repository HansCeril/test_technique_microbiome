from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from msio.backend.database.schemas import UserCreate, UserRead
from msio.backend.database.models import User
from msio.backend.database.session import get_db
from src.msio.backend.core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.

    This endpoint allows a new user to register by providing a
    username, email, and password.
    The password is securely hashed before being stored in the database.

    Args:
        user_in (UserCreate): Pydantic model containing the new user's
        username, email, and password.
        db (AsyncSession): Asynchronous database session (injected by FastAPI).

    Raises:
        HTTPException: 400 error if the username is already registered.

    Returns:
        UserRead: The created user, excluding sensitive fields such as the
        hashed password.
    """
    result = await db.execute(select(User).where(User.username == user_in.username))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = get_password_hash(user_in.password)
    user = User(
        username=user_in.username, email=user_in.email, hashed_password=hashed_pw
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Authenticate a user and return a JWT access token.

    This endpoint verifies a user's credentials. If valid, it returns a
    JWT access token that can be used to authenticate future requests.

    Args:
        form_data (OAuth2PasswordRequestForm): OAuth2 form with
        username and password.
        db (AsyncSession): Asynchronous database session (injected by FastAPI).

    Raises:
        HTTPException: 400 error if username or password is incorrect.

    Returns:
        dict: Access token and token type (bearer).
    """
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all registered users.
    returns all users stored in the db.

    Args:
        db (AsyncSession): Asynchronous SQLAlchemy database session.

    Returns:
        list[UserRead]: A list of user objects.
    """
    result = await db.execute(select(User))
    return result.scalars().all()
