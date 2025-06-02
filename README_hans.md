# test_technique_microbiome
Test technique CDI



poetry install

poetry run uvicorn src.msio.backend.main:app --reload --host 0.0.0.0 --port 8000
