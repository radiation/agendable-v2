# Official Kong image as parent
FROM kong:latest

# Install curl to make HTTP requests (if not already included)
RUN apk --no-cache add curl

# Copy scripts into the container
COPY scripts/entrypoint.sh /entrypoint.sh
COPY scripts/configure.sh /configure.sh

# Make the scripts executable
RUN chmod +x /entrypoint.sh /configure.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD ["kong", "start"]
