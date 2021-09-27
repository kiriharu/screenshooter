FROM python:3.9.4-slim-buster

WORKDIR /usr/src/api
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
RUN pip install --upgrade pip; \
    pip install poetry; \
    poetry config virtualenvs.create false; \
    poetry install --no-root --no-dev
CMD ["uvicorn", "screenshooter:app", "--port", "8001", "--host", "0.0.0.0", "--proxy-headers", "--no-use-colors"]