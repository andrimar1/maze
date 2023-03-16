FROM python:3.9

# Upgrading system and installing dependencies
RUN apt-get -y update && \
    pip install pipenv

ENV PROJECT_DIR /src

WORKDIR ${PROJECT_DIR}
COPY . ${PROJECT_DIR}/

RUN pipenv install --system --deploy

RUN mkdir -p ${PROJECT_DIR}/mnt
