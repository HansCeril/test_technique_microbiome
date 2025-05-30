FROM python:3.11.12-slim
WORKDIR /code/

COPY ./pyproject.toml ./poetry.lock* /code/
COPY . /code
ENV PYTHONPATH=/code/src

RUN bash -c "pip install poetry"

RUN bash -c "poetry install"

CMD bash -c "poetry run python -m uvicorn msio.backend.main:app --host 0.0.0.0 --port 8000 --reload"

