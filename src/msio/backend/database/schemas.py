from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class MetaboliteBase(BaseModel):
    feature: str
    identification_level: Optional[int] = Field(default=3, ge=1, le=5)
    id_inchi: Optional[str] = None
    cas_number: Optional[str] = None
    method: str
    sample_data: Optional[str] = None  # 'ND', 'NA', or float in string form


class MetaboliteCreate(MetaboliteBase):
    pass


class MetaboliteUpdate(MetaboliteBase):
    pass


class MetaboliteRead(MetaboliteBase):
    id: int
    uploader_user_id: Optional[int] = None

    class Config:
        orm_mode = True
