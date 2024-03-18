FROM python:3.10.12-alpine as builder

RUN pip install --no-cache-dir --upgrade pip
RUN apk --no-cache add \
    musl-dev  \
    gcc  \
    mariadb-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


FROM python:3.10.12-alpine

ENV TZ=Asia/Ho_Chi_Minh
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROCESSES 4

WORKDIR /app

RUN apk add --no-cache mariadb-dev
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY  . /app
