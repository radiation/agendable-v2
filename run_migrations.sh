#!/bin/bash

# Function to print usage instructions
print_usage() {
  echo "Usage: $0 [generate|apply] <service> [message]"
  echo ""
  echo "Commands:"
  echo "  generate   Generate a new migration script"
  echo "  apply      Apply all pending migrations"
  echo ""
  echo "Services:"
  echo "  user_service     Run command for the user service"
  echo "  meeting_service  Run command for the meeting service"
  echo ""
  echo "Examples:"
  echo "  Generate a new migration for the user service with a message:"
  echo "    $0 generate user_service \"Add new table\""
  echo ""
  echo "  Generate a new migration for the meeting service with a message:"
  echo "    $0 generate meeting_service \"Add new field\""
  echo ""
  echo "  Apply migrations for the user service:"
  echo "    $0 apply user_service"
  echo ""
  echo "  Apply migrations for the meeting service:"
  echo "    $0 apply meeting_service"
}

# Function to generate a new migration
generate_migration() {
  local service=$1
  local message=$2
  local db_url=$3

  docker-compose exec $service /bin/sh -c "
    export DATABASE_URL=$db_url
    alembic revision --autogenerate -m \"$message\"
  "
}

# Function to apply migrations
apply_migrations() {
  local service=$1
  local db_url=$2

  docker-compose exec $service /bin/sh -c "
    export DATABASE_URL=$db_url
    alembic upgrade head
  "
}

# Main script
if [ "$#" -lt 2 ]; then
  print_usage
  exit 1
fi

command=$1
service=$2

# Determine the database URL based on the service
case $service in
  user_service)
    db_url="postgresql://user:password@postgres:5432/user_db"
    ;;
  meeting_service)
    db_url="postgresql://user:password@postgres:5432/meeting_db"
    ;;
  *)
    echo "Unknown service: $service"
    exit 1
    ;;
esac

if [ "$command" = "generate" ]; then
  if [ -z "$3" ]; then
    print_usage
    exit 1
  fi
  message=$3
  generate_migration $service "$message" $db_url
elif [ "$command" = "apply" ]; then
  apply_migrations $service $db_url
else
  echo "Unknown command: $command"
  print_usage
  exit 1
fi
