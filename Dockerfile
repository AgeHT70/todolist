FROM python:3.10.9-slim

ENV POETRY_VERSION = 1.4.2

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /diplom
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
