FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all files from your repo to the container
COPY..

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# The Shell Form (no brackets) allows Railway to inject the dynamic $PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}