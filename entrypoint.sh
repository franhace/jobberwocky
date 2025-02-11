#!/bin/sh

create_database() {
    echo "Creating database tables..."
    python /app/app/db/create_db.py
    return $?
}

create_database
DB_STATUS=$?

if [ $DB_STATUS -eq 0 ]; then
    export DATABASE_READY=1
    echo "Database is ready."
else
    export DATABASE_READY=0
    echo "Database creation failed."
    exit 1
fi

echo "Starting the FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 80 --reload