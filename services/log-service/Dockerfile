# 1) Base runtime image
FROM python:3.12-slim

# 2) Prevents Python from buffering logs (better container logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3) Set working directory inside the container
WORKDIR /app

# 4) Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Copy application code
COPY app ./app
COPY scripts ./scripts

# 6) Expose the port uvicorn will listen on
EXPOSE 8000

# 7) Health check to ensure service is ready to accept traffic
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 CMD ["python", "scripts/container_healthcheck.py"]

# 8) Start the service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
