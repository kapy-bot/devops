# --- Stage 1: build dependencies into a venv -------------------------------
# Kept separate from the runtime stage so build tools (gcc, headers) needed
# to compile some Python packages never end up in the final image.
FROM python:3.12-slim AS builder

WORKDIR /build

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: runtime --------------------------------------------------------
FROM python:3.12-slim AS runtime

# Non-root user: the app never needs root inside the container.
RUN groupadd --system appuser && useradd --system --gid appuser appuser

WORKDIR /app

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY app ./app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
