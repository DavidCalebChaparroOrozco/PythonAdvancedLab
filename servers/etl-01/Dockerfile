FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql redis-server \
    && rm -rf /var/lib/apt/lists/*
RUN pg_conftool set listen_addresses '*'
CMD ["bash", "-c", "service postgresql start && redis-server --bind 0.0.0.0 --protected-mode no --daemonize yes && sleep infinity"]
