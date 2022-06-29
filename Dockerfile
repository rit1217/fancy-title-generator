# syntax=docker/dockerfile:1

# build
FROM python:3.10-slim-buster AS build
COPY requirements.txt .
COPY model_graph* model_graph/
COPY temp* temp/
RUN pip3 install \
    -r requirements.txt \
    && python3 -m model_graph


# run
FROM build AS run
WORKDIR /usr/src/app
ENV PYTHONPATH=/usr/src/app
ENV FLASK_APP=api/api.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY --from=build . /usr/src/app
COPY /api /usr/src/app/api
ENTRYPOINT ["flask", "run"]