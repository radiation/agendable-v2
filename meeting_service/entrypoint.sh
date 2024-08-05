#!/bin/bash

# Navigate to the migrations directory and run the migrations
cd /migrations
./run_migrations.sh apply

# Navigate back to the app directory
cd /app

# Execute the CMD from the Dockerfile, e.g., starting Uvicorn
exec "$@"
