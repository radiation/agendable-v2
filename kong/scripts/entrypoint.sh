#!/bin/bash

# Wait for PostgreSQL to be available
echo "Waiting for PostgreSQL to be available..."
while ! pg_isready -h postgres -p 5432 -U user; do
    sleep 1
done

# Run Kong migrations
echo "PostgreSQL is up - executing Kong migrations..."
kong migrations bootstrap || kong migrations up || true

# Start Kong
echo "Starting Kong..."
kong start

# Wait for Kong to be up
echo "Waiting for Kong to start..."
while ! curl -s http://localhost:8001/status; do
    sleep 1
done

echo "Kong is up - configuring services and routes..."

# Run script to configure services and routes
/bin/bash /create_routes.sh

echo "Kong configuration complete."
