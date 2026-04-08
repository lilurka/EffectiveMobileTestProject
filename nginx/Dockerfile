FROM nginx:1.27-alpine

LABEL maintainer="Effective Mobile DevOps" \
      description="Nginx reverse proxy + static frontend"

# Remove default config and replace with ours
RUN rm /etc/nginx/conf.d/default.conf

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/app.conf

EXPOSE 80

HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost/nginx-health || exit 1