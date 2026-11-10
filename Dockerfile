# Build the frontend
FROM node:22-bookworm-slim AS frontend

WORKDIR /app/www
COPY www/package.json www/package-lock.json ./
RUN npm ci
COPY www/ ./
RUN npm run build -- --outDir /app/build

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install nginx and supervisor
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx supervisor \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /etc/nginx/sites-enabled/default

# Install python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into image
COPY . ./
COPY --from=frontend /app/build ./build
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/imgserve.conf

# Expose port
EXPOSE 8080

# Run server
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]