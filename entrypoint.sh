#!/bin/sh

create_database() {
    echo "Creating database tables..."
    python /app/app/db/create_db.py
    return $?
}

seed_database() {
    if [ -f app/db/seed_db.py ]; then
        python app/db/seed_db.py
        return $?
    else
        echo "Error: seed_db.py not found at ./db/seed_db.py"
        return 1
    fi
}

create_database
echo "Wainting a few seconds before creating db..."
sleep 1
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