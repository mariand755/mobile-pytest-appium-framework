FROM python:3.12-slim

WORKDIR /work

# system deps (curl for download scripts; unzip often handy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /work/requirements.txt
RUN pip install --no-cache-dir -r /work/requirements.txt

COPY docker/entrypoint.sh /work/docker/entrypoint.sh
RUN chmod +x /work/docker/entrypoint.sh

# copy project into container
COPY . /work

ENTRYPOINT ["/work/docker/entrypoint.sh"]

