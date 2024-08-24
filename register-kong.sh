KONG_URL="http://localhost:8001"
USER_SERVICE_URL="http://localhost:8004"
MEETING_SERVICE_URL="http://localhost:8005"

# Add user_service
curl -i -X POST \
  --url ${KONG_URL}/services/ \
  --data "name=user_service" \
  --data "url=${USER_SERVICE_URL}"

# Add meeting_service
curl -i -X POST \
  --url ${KONG_URL}/services/ \
  --data "name=meeting_service" \
  --data "url=${MEETING_SERVICE_URL}"

# Route for authentication related paths
curl -i -X POST \
  --url ${KONG_URL}/services/user_service/routes \
  --data "paths[]=/auth" \
  --data "strip_path=false" \
  --data "name=auth_route"

# Route for user management paths
curl -i -X POST \
  --url ${KONG_URL}/services/user_service/routes \
  --data "paths[]=/users" \
  --data "strip_path=false" \
  --data "name=users_route"

# Add meeting_service route
curl -i -X POST \
  --url ${KONG_URL}/services/meeting_service/routes \
  --data "paths[]=/meeting"
