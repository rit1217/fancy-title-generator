# syntax=docker/dockerfile:1


# base
FROM python:3.10-slim-buster AS base


# build
FROM base AS build
ENV BUILD_DIR=/build \
    PYTHONPATH=/build
WORKDIR $BUILD_DIR
COPY requirements.txt .
COPY model_graph* model_graph/
COPY temp* temp/
RUN pip3 install --target $BUILD_DIR\
    -r requirements.txt \
    && python3 -m model_graph


# run
FROM base AS run
ENV APP_DIR=/usr/src/app\
    PYTHONPATH=/usr/src/app
ENV FLASK_APP=api/api.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY --from=build /build $PYTHONPATH
COPY /api $APP_DIR/api
COPY /model_graph $APP_DIR/model_graph
WORKDIR $APP_DIR
ENTRYPOINT ["python3", "-m", "flask", "run"]