FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

ENV TQDM_POSITION=-1
ENV TZ="Asia/Ho_Chi_Minh"
ENV PROMETHEUS_MULTIPROC_DIR=/app/prometheus
RUN mkdir -p $PROMETHEUS_MULTIPROC_DIR && chmod 777 -R $PROMETHEUS_MULTIPROC_DIR

RUN mkdir -p /vault/secrets
RUN mkdir -p /vault/config
COPY template.tpl /vault/config/template.tpl
COPY vault-agent-config.hcl /vault/config/vault-agent-config.hcl

COPY --from=hashicorp/vault:latest /bin/vault /bin/vault

RUN apt-get update -q -y && \
    apt-get install -q -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/

COPY requirements.txt requirements.txt

RUN pip3 install --disable-pip-version-check --no-cache-dir -r requirements.txt

# add source code
COPY bin /app/bin/
COPY src /app/src/
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x *.sh
RUN chmod a+x,g+x /app/bin/*
RUN chmod +x /app/entrypoint.sh

EXPOSE 8888

ENTRYPOINT ["/app/entrypoint.sh"]
