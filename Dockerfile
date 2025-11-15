# 1. Start from an official, lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --- THIS IS THE FIX ---
# Tell Python to look for modules in the /app directory
ENV PYTHONPATH /app
# ---------------------

# 2. Install system-level dependencies
# - postgresql-client is needed for the 'psql' command in our entrypoint script
# - build-essential & libpq-dev are needed to build 'psycopg2-binary'
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev postgresql-client \
    && apt-get clean

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy and install Python requirements
# We copy this file first to take advantage of Docker's caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Make the entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# 7. Set the entrypoint script to run
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# 8. The default command to run after the entrypoint
# This is what the 'exec "$@"' line in the script will run
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]