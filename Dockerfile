FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all files from your repo to the container (Note the spaces between dots!)
COPY..

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the application using Shell Form to properly expand the $PORT variable
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
