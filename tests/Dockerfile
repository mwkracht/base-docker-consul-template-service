FROM python:3.6-alpine

LABEL maintainer="Matt Kracht" \
      email="mwkracht@gmail.com"

COPY requirements.txt /requirements.txt

# g++ needed at runtime for zmq dependency
RUN apk add --no-cache --virtual .build-deps gcc python2-dev musl-dev linux-headers && \
    apk add --no-cache g++ && \
    pip install -r requirements.txt && \
    apk del --no-cache .build-deps && \
    rm -rf /var/cache/apk/*

COPY tests /tests

# By default keep docker container running indefinitely. This will allow for manual running
# of tests inside of container (and also manual debugging). For automated tests this command
# shoudl be overridden.
CMD ["tail", "-f", "/dev/null"]
