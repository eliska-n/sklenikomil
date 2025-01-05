FROM alpine:3.18 AS building

RUN set -ex \
  && apk update \
  && apk upgrade

RUN apk add --no-cache \
  python3 \
  py3-pip \
  git \
  python3-dev \
  libffi-dev \
  openssl-dev \
  gcc \
  g++ \
  libstdc++ \
  musl-dev

RUN pip3 install --upgrade pip
RUN pip3 install motor git+https://github.com/TeskaLabs/asab.git

RUN mkdir -p /app/sklenikomil-be

COPY . /app/sklenikomil-be

FROM alpine:3.18 AS shiping

RUN apk add --no-cache python3

COPY --from=building /usr/lib/python3.11/site-packages /usr/lib/python3.11/site-packages

COPY ./sklenikomil           /app/sklenikomil-be/sklenikomil
COPY ./sklenikomil.py        /app/sklenikomil-be/sklenikomil.py

RUN set -ex \
  && mkdir /conf \
  && touch conf/sklenikomil.conf

WORKDIR /app/sklenikomil-be
CMD ["python3", "sklenikomil.py", "-c", "/conf/sklenikomil.conf"]
