import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from msio.backend.database.models import Metabolite
from ETL.parser import parse_csv, Path

# Local Session postgres db
POSTGRES_URI = "postgresql+asyncpg://admin:admin@localhost:5432/backend"
engine = create_async_engine(POSTGRES_URI, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def insert_data():
    """
    Parse and validate a CSV file containing metabolite data,
    then insert the data
    into a PostgreSQL database asynchronously using SQLAlchemy ORM.

    Steps:
    - Read and validate CSV data using the `parse_csv` function
    - Convert each validated metabolik data into a `Metabolite` ORM instance.
    - Add all ORM instances to the session and commit the transaction.

    Raises:
        ValueError: If rows is invalid or inconsistent.
        SQLAlchemyError: If the insertion fails db errror.
    """
    csv_path = Path("data/MetabolitesData_inputDataForTEst.csv")
    entries = parse_csv(csv_path)

    orm_objects = [
        Metabolite(
            feature=e.feature,
            identification_level=e.identification_level,
            id_inchi=e.id_inchi,
            cas_number=e.cas_number,
            method=e.method,
            sample_data=e.sample_data,
        )
        for e in entries
    ]

    async with SessionLocal() as session:
        async with session.begin():
            session.add_all(orm_objects)
        print(f"Inserted {len(orm_objects)} metabolites into the database.")


if __name__ == "__main__":
    try:
        asyncio.run(insert_data())
    except Exception as e:
        print(f"Error: {e}")
