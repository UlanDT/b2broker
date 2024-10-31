FROM python:3.11.4

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential python3-dev

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock Makefile /app/
RUN make install-deploy

COPY . /app/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
