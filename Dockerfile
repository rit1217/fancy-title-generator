# syntax=docker/dockerfile:1.2


# base
FROM python:3.10.2-slim-buster AS base


# build
FROM base AS build
ENV BUILD_DIR=/build \
    PYTHONPATH=/build
WORKDIR $BUILD_DIR
COPY requirements.txt .
RUN pip3 wheel --wheel-dir=/wheels -r requirements.txt


# prod
FROM base AS prod
ENV APP_DIR=/usr/src/app\
    PYTHONPATH=/usr/src/app
COPY . $APP_DIR
WORKDIR $APP_DIR
ENV FLASK_APP=./api/api.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY --from=build /wheels /wheels
RUN pip3 install \
  --no-index \
  --no-cache-dir \
  --find-links=/wheels \
  -r requirements.txt \
  && python3 -m model_graph
ENTRYPOINT ["python3", "-m" ,"flask", "run"]