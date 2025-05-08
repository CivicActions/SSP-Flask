FROM ghcr.io/civicactions/pyction:latest

WORKDIR /app

ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -u ${USER_ID} -g appuser -s /bin/bash -m appuser

RUN chown -R appuser:appuser /app

USER appuser

COPY app ./app

COPY pyproject.toml uv.lock ./
COPY .env ./

RUN uv sync --no-dev

EXPOSE 5000

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["uv", "run", "flask", "run"]
