FROM python:3.11-alpine AS base

FROM base AS builder

# Give desired Username below
ARG user=provenclub

RUN adduser -D -g '' ${user} && \
    apk update && \
    apk upgrade --no-cache && \
    apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev g++ \
    libffi-dev jpeg-dev zlib-dev jq sox

# Switch User
USER ${user}

COPY requirements.txt ./

# Update PATH environment variable
ENV PATH=/home/${user}/.local/bin:$PATH

# Install requirements
RUN python3.11 -m pip install --upgrade pip --user && python3.11 -m pip install -r requirements.txt --user

USER root
RUN rm requirements.txt


FROM base

ARG user=provenclub

WORKDIR /home/${user}

COPY --from=builder /home/${user}/.local/ /usr/local

COPY provenclub/ /home/${user}

RUN apk add postgresql-libs gcc libc-dev sox

RUN apk add curl && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && apk del curl

ENV PATH=/usr/local:$PATH


EXPOSE 8007

ENV POSTGRES_REMOTE_PORT=5432 \
    POSTGRES_REMOTE_HOST=host.docker.internal

CMD ["gunicorn", "provenclub.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "180"]
