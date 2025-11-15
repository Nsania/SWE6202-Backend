#!/bin/sh

# This script waits for the PostgreSQL database to be ready
# before starting the Django application.

DB_HOST="db"
DB_NAME="$POSTGRES_DB"
DB_USER="$POSTGRES_USER"
DB_PASSWORD="$POSTGRES_PASSWORD"

echo "Waiting for PostgreSQL at $DB_HOST..."

# We use 'psql' to ping the database
# 'psql' is not in our Python image, so we must add it in the Dockerfile
while ! psql "host=$DB_HOST user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME" -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"

# Run Django migrations
echo "Running database migrations..."
python manage.py migrate

# Now, execute the main command (what's in the Dockerfile's CMD)
# This will be "python manage.py runserver 0.0.0.0:8000"
exec "$@"