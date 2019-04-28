FROM python:3.6-alpine

LABEL maintainer="Matt Kracht" \
      email="mwkracht@gmail.com" \
      description="Example containerized app which generates own configruation using consul-template"

ARG CONSUL_TEMPLATE_VERSION=0.20.0
ADD https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip /

RUN unzip consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip && \
    mv consul-template /usr/local/bin/consul-template && \
    rm -rf /consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip && \
    apk add --no-cache curl

ENV INSTALL_PATH /opt/simple_app
COPY src $INSTALL_PATH

# g++ needed at runtime for zmq dependency
RUN apk add --no-cache --virtual .build-deps gcc python2-dev musl-dev linux-headers && \
    apk add --no-cache supervisor g++ && \
    pip install $INSTALL_PATH/simple_app supervisor && \
    apk del --no-cache .build-deps && \
    rm -rf /var/cache/apk/*

COPY root /

ENTRYPOINT ["/bin/entrypoint.sh"]
