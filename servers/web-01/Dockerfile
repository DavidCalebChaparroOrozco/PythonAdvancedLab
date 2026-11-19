FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx redis-server \
    && rm -rf /var/lib/apt/lists/*
RUN sed -i '/listen \[::\]/d' /etc/nginx/sites-enabled/default
CMD ["bash", "-c", "redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes && nginx -g 'daemon off;'"]
