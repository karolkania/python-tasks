FROM python:3.9

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /srv

COPY pyproject.toml poetry.lock /srv/

# Install dependencies:
RUN pip install poetry==1.1.4
RUN poetry config virtualenvs.create false
RUN poetry install -n --no-root --no-dev

# Commented by default for local development
# Uncomment if willing to distribute
# COPY . /srv

# Overwritten by docker-compose for local development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
