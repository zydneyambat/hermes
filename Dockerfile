FROM python:3.9-slim as cli

WORKDIR /opt/hermes

RUN apt update && \
    apt-get upgrade -y && \
    pip install --upgrade pip pipenv

COPY . .

RUN pipenv install --deploy --system

ENTRYPOINT ["/usr/local/bin/hermes"]


FROM cli as test

RUN pipenv install -d --system

ENTRYPOINT ["pipenv", "run", "pytest", "-vvv"]
