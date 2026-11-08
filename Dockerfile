# Builder stage to install dependencies
FROM python:3.14-slim AS builder
WORKDIR /app
COPY requirements.txt .

RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
        fi

# Final stage to run the application
FROM python:3.14-alpine
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
WORKDIR /app
COPY . .

# Set non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
EXPOSE 5000

CMD ["ddtrace-run", "python3", "-m", "app.py"]
