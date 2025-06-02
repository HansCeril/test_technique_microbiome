from typing import Optional
from pydantic import BaseModel, field_validator, model_validator


class MetaboliteBase(BaseModel):
    """
    Base schema for metabolite fields.
    """

    feature: str
    identification_level: int = 3
    id_inchi: Optional[str] = None
    cas_number: Optional[str] = None
    method: str
    sample_data: Optional[float] = None


class MetaboliteCreate(MetaboliteBase):
    """
    Schema for creating a new metabolite.

    - Ensures sample_data is a float or None
    - Ensures at least one identifier (InChI or CAS) is present
    - Cleans empty strings as None
    """

    @field_validator("sample_data", mode="before")
    @classmethod
    def parse_sample_data(cls, v):
        """
        Converts raw input into a float or None.

        Args:
            v (Any): Raw value from input.

        Raises:
            ValueError: If input error string.

        Returns:
            float | None: Parsed value or None for "ND", "NA", or empty.
        """
        if isinstance(v, str):
            if v.strip().upper() in {"ND", "NA", ""}:
                return None
            try:
                return float(v)
            except ValueError:
                raise ValueError(f"Invalid float value for sample_data: {v}")
        return v

    @field_validator("id_inchi", "cas_number", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        """
        Converts empty string values into None.

        Args:
            v (str | None): Raw input value.

        Returns:
            str | None: None if empty, otherwise the input value.
        """
        return v if v and v.strip() else None

    @field_validator("identification_level", mode="before")
    @classmethod
    def default_identification_level(cls, v):
        """
        Ensures identification_level is cast to int and defaults to 3.

        Args:
            v (Any): Raw value.

        Returns:
            int: Validated identification level.
        """
        return int(v) if v else 3

    @model_validator(mode="after")
    def check_id_or_cas(self):
        """
        Validates presence of at least one identifier.

        Raises:
            ValueError: If both id_inchi and cas_number are missing.

        Returns:
            MetaboliteCreate: The validated object.
        """
        if not self.id_inchi and not self.cas_number:
            raise ValueError("Either ID_InChI or CAS_number must be provided.")
        return self


class MetaboliteRead(MetaboliteBase):
    """
    Schema for reading a metabolite record from the database.

    Includes all base fields plus:
    - id: Unique DB identifier.
    - uploader_id: ID of the user who uploaded the record.
    """

    id: int
    uploader_id: Optional[int] = None

    class Config:
        orm_mode = True
