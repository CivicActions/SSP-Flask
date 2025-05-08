FROM ghcr.io/civicactions/pyction:latest

COPY app ./app
COPY pyproject.toml uv.lock ./
COPY ssp/ ./ssp
COPY .env .

RUN uv venv .dockerenv
RUN uv sync --no-dev

WORKDIR /app

EXPOSE 5000

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["uv", "run", "flask", "run"]
