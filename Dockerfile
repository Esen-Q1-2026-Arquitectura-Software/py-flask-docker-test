# =============================================================================
# Stage 1 — base: install all dependencies via uv
# =============================================================================
FROM python:3.13-slim AS base

WORKDIR /app

# Install uv (fast Python package manager)
RUN pip install --no-cache-dir uv

# Copy dependency manifests and install (frozen = exact versions from uv.lock)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# =============================================================================
# Stage 2 — test: copy source and run pytest
#   If any test fails the build exits non-zero here and goes no further.
# =============================================================================
FROM base AS test

# Copy the entire project into the image
COPY . .

RUN uv run pytest tests/ -v

# =============================================================================
# Stage 3 — production: only reachable if the test stage passed
#   COPY --from=test creates a hard dependency: Docker must successfully
#   complete the test stage before it can build this stage.
# =============================================================================
FROM base AS production

# This COPY is what gates the build — if the test stage failed, this is
# never executed and docker compose up will report a build error.
COPY --from=test /app /app

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["uv", "run", "python", "main.py"]
