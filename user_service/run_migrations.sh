#!/bin/bash

# Function to generate a new migration
generate_migration() {
  local message=$1
  local db_url=$2

  alembic -c /migrations/alembic.ini revision --autogenerate -m "$message"
}

# Function to apply migrations
apply_migrations() {
  local db_url=$1

  alembic -c /migrations/alembic.ini upgrade head
}

# Main script
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 [generate|apply] <message>"
  exit 1
fi

command=$1

# Determine the database URL based on the service directory
if [[ "$PWD" == *"user_service"* ]]; then
  db_url="postgresql://user:password@postgres:5432/user_db"
elif [[ "$PWD" == *"meeting_service"* ]]; then
  db_url="postgresql://user:password@postgres:5432/meeting_db"
else
  echo "Unknown service directory: $PWD"
  exit 1
fi

if [ "$command" = "generate" ]; then
  if [ -z "$2" ]; then
    echo "Usage: $0 generate <message>"
    exit 1
  fi
  message=$2
  generate_migration "$message" $db_url
elif [ "$command" = "apply" ]; then
  apply_migrations $db_url
else
  echo "Unknown command: $command"
  exit 1
fi
