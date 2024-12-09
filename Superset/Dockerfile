FROM python:3.11.11-slim-bullseye

# Configure environment
# superset/gunicorn recommended defaults:
# - https://superset.apache.org/docs/installation/configuring-superset#running-on-a-wsgi-http-server
# - https://docs.gunicorn.org/en/latest/configure.html
ENV FLASK_APP=superset
ENV GUNICORN_BIND=0.0.0.0:8088
ENV GUNICORN_LIMIT_REQUEST_FIELD_SIZE=8190
ENV GUNICORN_LIMIT_REQUEST_LINE=4094
ENV GUNICORN_THREADS=4
ENV GUNICORN_TIMEOUT=120
ENV GUNICORN_WORKERS=4
ENV GUNICORN_WORKER_CLASS=gevent
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONPATH=/etc/superset:/home/superset
ENV SUPERSET_HOME=/var/lib/superset
ENV GUNICORN_CMD_ARGS="--bind $GUNICORN_BIND --limit-request-field_size $GUNICORN_LIMIT_REQUEST_FIELD_SIZE --limit-request-line $GUNICORN_LIMIT_REQUEST_LINE --threads $GUNICORN_THREADS --timeout $GUNICORN_TIMEOUT --workers $GUNICORN_WORKERS --worker-class $GUNICORN_WORKER_CLASS"


# Configure filesystem

VOLUME /etc/superset
VOLUME /home/superset
VOLUME /var/lib/superset

COPY bin /usr/local/bin
COPY superset_config.py /home/superset/superset_config.py

ENV SUPERSET_CONFIG_PATH=/home/superset/superset_config.py

# Create superset user & install dependencies
WORKDIR /home/superset
RUN groupadd supergroup
RUN useradd -U -G supergroup superset && \
    mkdir -p $SUPERSET_HOME && \
    mkdir -p /etc/superset && \
    chown -R superset:superset $SUPERSET_HOME && \
    chown -R superset:superset /home/superset && \
    chown -R superset:superset /etc/superset && \
    apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    curl &&\
    apt-get clean && \
    pip install -U pip

# Install pips
COPY requirements*.txt ./
RUN pip install -r requirements.txt

# Configure application
EXPOSE 8088
USER superset
HEALTHCHECK CMD ["curl", "-f", "http://localhost:8088/health"]
CMD ["gunicorn", "superset.app:create_app()"]