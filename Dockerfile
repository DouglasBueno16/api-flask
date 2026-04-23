# Builder stage to install dependencies
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .

RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
        fi

# Final stage to run the application
FROM python:3.12-slim
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
WORKDIR /app
COPY . .

# Set non-root user for security
RUN useradd -m appuser
USER appuser
EXPOSE 5000

CMD ["python", "main.py"]
