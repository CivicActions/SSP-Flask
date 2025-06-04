FROM ghcr.io/civicactions/pyction:latest

COPY app ./app
COPY pyproject.toml uv.lock ./
COPY ssp/ ./ssp

RUN uv venv .dockerenv
RUN uv sync --no-dev

RUN chmod 777 /ssp
RUN mkdir /logs && chmod 777 /logs

WORKDIR /app

EXPOSE 5000

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["uv", "run", "flask", "run", "--host=0.0.0.0"]
