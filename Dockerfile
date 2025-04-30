FROM ghcr.io/civicactions/pyction:latest

WORKDIR /app

COPY . .

RUN uv sync --no-dev

EXPOSE 5000

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["uv", "run", "flask", "run"]
