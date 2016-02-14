FROM python:3.4
MAINTAINER Vincent Fretin <vincentfretin@ecreall.com>

# grab gosu for easy step-down from root
RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN arch="$(dpkg --print-architecture)" \
    && set -x \
    && curl -o /usr/local/bin/gosu -fSL "https://github.com/tianon/gosu/releases/download/1.7/gosu-$arch" \
    && curl -o /usr/local/bin/gosu.asc -fSL "https://github.com/tianon/gosu/releases/download/1.7/gosu-$arch.asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu

RUN mkdir -p /app
COPY . /app/
RUN test -d /app/cache/eggs && cp -rf /app/cache/eggs /app/eggs || exit 0
RUN test -d /app/cache/src && cp -rf /app/cache/src /app/src || exit 0
COPY start.bash /start
RUN chmod +x /start /app/copy_to_cache_and_start.sh

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y varnish && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --quiet --gid "1000" "u1000" && \
    adduser \
        --shell /bin/bash \
        --disabled-password \
        --force-badname \
        --no-create-home \
        --uid "1000" \
        --gid "1000" \
        --gecos '' \
        --quiet \
        --home "/app" \
        "u1000"
RUN pip install zc.buildout==2.5.0
RUN mkdir -p /app/cache/eggs /app/cache/src
RUN chown -R u1000:u1000 /app
USER u1000
WORKDIR /app
RUN buildout bootstrap && ./bin/buildout -c heroku.cfg
USER root

EXPOSE 5000
VOLUME /app/var
VOLUME /app/cache

CMD ["/app/copy_to_cache_and_start.sh"]
