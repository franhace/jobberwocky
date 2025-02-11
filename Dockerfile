FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Install SQLite (if needed)
RUN apt-get update && apt-get install -y sqlite3

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code and environment variables
COPY ./app /app/app
COPY ./tests /app/test
COPY ./.env /app/.env

# Copy entrypoint script and make it executable
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set environment variable for database readiness
ENV DATABASE_READY=0

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]