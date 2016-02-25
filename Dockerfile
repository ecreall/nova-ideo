FROM python:3.4
MAINTAINER Vincent Fretin <vincentfretin@ecreall.com>

ARG userid=1000

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y varnish && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --quiet --gid $userid "u1000" && \
    adduser \
        --shell /bin/bash \
        --disabled-password \
        --force-badname \
        --no-create-home \
        --uid $userid \
        --gid $userid \
        --gecos '' \
        --quiet \
        --home "/app" \
        "u1000"
RUN pip install zc.buildout==2.5.0

# grab gosu for easy step-down from root
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN arch="$(dpkg --print-architecture)" \
    && set -x \
    && curl -o /usr/local/bin/gosu -fSL "https://github.com/tianon/gosu/releases/download/1.7/gosu-$arch" \
    && curl -o /usr/local/bin/gosu.asc -fSL "https://github.com/tianon/gosu/releases/download/1.7/gosu-$arch.asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu

RUN mkdir -p /app/cache
COPY . /app/
COPY start.bash /start
RUN chown -R u1000:u1000 /app

USER u1000
WORKDIR /app

RUN mkdir -p -m 700 /app/.ssh && \
    echo "|1|mkhJkTqJT7XEFCg9zJ6vXr9F7KM=|1ihCQCq4xl9SQDtCAqwp4auiRIk= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNn6VI+Ekg/iOz3bZL6bb35tj6fOjmmMOvkw592XDXy+bSes+2qHhcA3uOg5/wEtmRaK583uZH/CJ4512BpLb7M=" >> /app/.ssh/known_hosts && \
    echo "|1|VmfmXO+MNtehwEnpYIEHO7zfvm8=|ya5Yt/ILBv/gMHQLAfSu2tOWO2I= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNn6VI+Ekg/iOz3bZL6bb35tj6fOjmmMOvkw592XDXy+bSes+2qHhcA3uOg5/wEtmRaK583uZH/CJ4512BpLb7M=" >> /app/.ssh/known_hosts
RUN buildout bootstrap -c heroku.cfg
# bin/buildout -c heroku.cfg is done outside this build

USER root
EXPOSE 5000
VOLUME /app/var

CMD ["/start"]
