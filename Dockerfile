# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first (better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies into /app/.venv (no dev deps)
RUN uv sync --frozen --no-dev

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Copy the venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY app/        ./app/
COPY main.py     ./main.py
COPY data/       ./data/

# Make sure Python uses the venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose the default Litestar port
EXPOSE 8000

# Stream logs to stdout (PYTHONUNBUFFERED=1 already handles this)
# Run the Litestar app
CMD ["litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]
