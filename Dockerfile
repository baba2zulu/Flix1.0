FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# COPY (space). (space). copies your project files to the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Start the application using Shell Form (no brackets) 
# This is necessary for Railway to expand the $PORT variable at runtime
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
