#!/bin/sh

DB_PATH="/app/app/db/jobs.db"

delete_database() {
    if [ -f "$DB_PATH" ]; then
        echo "Deleting existing database at $DB_PATH..."
        rm -f "$DB_PATH"
        if [ $? -ne 0 ]; then
            echo "Error: Failed to delete existing database."
            exit 1
        fi
    else
        echo "No existing database found at $DB_PATH. Proceeding..."
    fi
}

create_database() {
    echo "Creating database tables..."
    python app/db/create_db.py
    return $?
}

seed_database() {
    if [ -f /app/app/db/seed_db.py ]; then
        echo "Seeding database..."
        python /app/app/db/seed_db.py
        return $?
    else
        echo "Error: seed_db.py not found at /app/app/db/seed_db.py"
        return 1
    fi
}

run_tests() {
    echo "Running tests..."
    if pytest; then
        echo "All tests passed."
    else
        echo "Tests failed!"
        exit 1
    fi
}

run_tests
sleep 2
delete_database
create_database
DB_STATUS=$?

if [ $DB_STATUS -eq 0 ]; then
    export DATABASE_READY=1
    echo "Database is ready."

    seed_database
    SEED_STATUS=$?

    if [ $SEED_STATUS -eq 0 ]; then
        echo "Database seeding completed successfully."
    else
        echo "Database seeding failed."
        exit 1
    fi
else
    export DATABASE_READY=0
    echo "Database creation failed."
    exit 1
fi

echo "Starting the FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 80 --reload