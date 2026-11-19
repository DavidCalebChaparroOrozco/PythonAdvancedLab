FROM debian:12
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql \
    && rm -rf /var/lib/apt/lists/*
RUN pg_conftool set listen_addresses '*'
CMD ["bash", "-c", "service postgresql start && sleep infinity"]
