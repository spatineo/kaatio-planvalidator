ARG PYTHON_VERSION=3.10.6

FROM python:${PYTHON_VERSION}-slim-bullseye AS release_base
RUN mkdir /opt/app
ENV APP_HOME=/opt/app \
    APP_VENV=/opt/venv \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
ENV PATH=${APP_VENV}/bin:${PATH}
RUN python3 -m venv ${APP_VENV}
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt install --assume-yes --quiet \
    gdal-bin \
    && apt --assume-yes --quiet autoremove \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR ${APP_HOME}

FROM release_base AS release_build
RUN pip install poetry
ENV POETRY_VIRTUALENVS_CREATE=False
COPY . ${APP_HOME}/
RUN poetry install
RUN pytest \
    && poetry build --format wheel

FROM release_base AS release_dist
COPY --from=release_build ${APP_HOME}/dist/*.whl ${APP_HOME}/
RUN pip install ${APP_HOME}/*.whl
COPY docker/gunicorn/bin/* /usr/bin/
RUN chmod +x /usr/bin/docker*
ENTRYPOINT ["docker-entrypoint.sh"]
EXPOSE 8000
CMD ["docker-cmd.sh"]
