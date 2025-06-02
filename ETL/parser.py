import csv
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, field_validator, model_validator


class MetaboliteInput(BaseModel):
    """
    Pydantic model for validating and parsing a single row of metabolite
    data from a CSV file.

    Attributes:
        feature (str): Name of the metabolite feature.
        identification_level (int): Identification level.
        id_inchi (str | None): InChI identifier of the metabolite (optional).
        cas_number (str | None): CAS number of the metabolite (optional).
        method (str): Method used to identify the metabolite.
        sample_data (float | None): Sample quantity;
                    can be a float, "ND", "NA", or empty (converted to None).

    Raises:
        ValueError: If both `id_inchi` and `cas_number` are missing.
        ValueError: If `sample_data` cannot be converted to
                    float when not "ND", "NA", or empty.
    """

    feature: str = Field(..., alias="Features")
    identification_level: int = Field(default=3, alias="Identification_level")
    id_inchi: str | None = Field(default=None, alias="ID_InChI")
    cas_number: str | None = Field(default=None, alias="CAS_number")
    method: str = Field(..., alias="Method")
    sample_data: float | None = Field(default=None, alias="Sample Data")

    @field_validator("sample_data", mode="before")
    @classmethod
    def parse_sample_data(cls, v):
        """
        Converts raw sample data into a float or None.

        Args:
            v (Any): Raw input from the CSV.

        Raises:
            ValueError: If the input is not a valid float or acceptable string
            (ND, NA, empty).

        Returns:
            float | None: Parsed float or None if data is "ND", "NA", or empty.
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
        Converts empty strings to None.

        Args:
            v (str | None): Input string.

        Returns:
            str | None: None if input is empty, otherwise unchanged.
        """
        return v if v and v.strip() else None

    @field_validator("identification_level", mode="before")
    @classmethod
    def default_identification_level(cls, v):
        """
        Ensures identification level is an integer; defaults to 3 if missing.

        Args:
            v (Any): Input value.

        Returns:
            int: Validated identification level.
        """
        return int(v) if v else 3

    @model_validator(mode="after")
    def check_id_or_cas(self):
        """
        Validates that at least one of `id_inchi` or `cas_number` is present.

        Raises:
            ValueError: If both fields are missing.

        Returns:
            MetaboliteInput: The validated model.
        """
        if not self.id_inchi and not self.cas_number:
            raise ValueError("Either ID_InChI or CAS_number must be provided.")
        return self


def parse_csv(file_path: Path) -> List[MetaboliteInput]:
    """
    Parses and validates a CSV file of metabolite data into a list of
    `MetaboliteInput` instances.

    Args:
        file_path (Path): Path to the CSV file.

    Raises:
        ValueError: If a row has invalid or inconsistent data.
        ValueError: If a feature is linked to multiple IDs or vice versa.

    Returns:
        List[MetaboliteInput]: A list of valid metabolite inputs.
    """
    seen_features = {}
    seen_ids = {}

    with file_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        data = []

        for i, row in enumerate(reader, 2):
            try:
                input_data = MetaboliteInput(**row)

                id_key = input_data.id_inchi or input_data.cas_number
                if id_key in seen_ids and seen_ids[id_key] != input_data.feature:
                    raise ValueError(
                        f"[Line {i}] ID already used for another \
                                     feature"
                    )
                if (
                    input_data.feature in seen_features
                    and seen_features[input_data.feature] != id_key
                ):
                    raise ValueError(
                        f"[Line {i}] Feature already linked to \
                                     another ID"
                    )

                seen_ids[id_key] = input_data.feature
                seen_features[input_data.feature] = id_key

                data.append(input_data)
            except Exception as e:
                raise ValueError(f"Error in line {i}: {e}")

    return data


if __name__ == "__main__":
    csv_path = Path("data/MetabolitesData_inputDataForTEst.csv")

    try:
        entries = parse_csv(csv_path)
        print(f"Parsed {len(entries)} rows successfully.")
        for data in entries[:5]:
            print(data.model_dump())
    except Exception as e:
        print(f"Error while parsing: {e}")
