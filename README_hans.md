# test_technique_microbiome
Test technique CDI



poetry install

poetry run uvicorn src.msio.backend.main:app --reload --host 0.0.0.0 --port 8000


poetry run alembic revision --autogenerate -m "change to float sample_data"
poetry run alembic upgrade head

GET /metabolites/

POST /metabolites/

GET /metabolites/{id}

PUT /metabolites/{id}

DELETE /metabolites/{id}