# ── Stage 1: builder (installs nothing extra, just validates syntax) ──────────
FROM python:3.12-alpine AS builder

WORKDIR /app
COPY app.py .

# Verify the script is valid Python before we ship it
RUN python -m py_compile app.py && echo "Syntax OK"

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.12-alpine

LABEL maintainer="Effective Mobile DevOps" \
      description="Simple Python HTTP backend" \
      version="1.0"


# Install wget for healthcheck
RUN apk add --no-cache wget

# Run as non-root user for security hardening
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /app/app.py .

# Own files by non-root user
RUN chown -R appuser:appgroup /app

USER appuser

# Document the port (does not publish it)
EXPOSE 8080

ENV APP_PORT=8080 \
    APP_HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:8080/health || exit 1

CMD ["python", "app.py"]