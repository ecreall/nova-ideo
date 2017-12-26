FROM python:3.6

ARG userid=1000
ARG run_buildout=true

# varnish 4.1 repo has a package for debian jessie, debian stretch,
# ubuntu xenial (16.04), but not ubuntu zesty (17.04) so defaults to varnish 5.0.0 from ubuntu repo.
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl git libzmq3-dev libyaml-dev apt-transport-https lsb-release && \
    curl -L https://packagecloud.io/varnishcache/varnish41/gpgkey | apt-key add - && \
    oslower=$(lsb_release -s -i | tr '[:upper:]' '[:lower:]') && \
    oscodename=$(lsb_release -s -c) && \
    echo "Package: varnish" >/etc/apt/preferences.d/varnish && \
    echo "Pin: release l=varnish41" >>/etc/apt/preferences.d/varnish && \
    echo "Pin-Priority: 999" >>/etc/apt/preferences.d/varnish && \
    (test $oscodename != 'zesty' && echo "deb https://packagecloud.io/varnishcache/varnish41/${oslower}/ ${oscodename} main" > /etc/apt/sources.list.d/varnishcache_varnish41.list || true) && \
    apt-get update && \
    apt-get install -y varnish && \
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
RUN pip3 install --disable-pip-version-check --no-cache-dir zc.buildout==2.9.5 setuptools==32.2.0 && pip3 uninstall -y six || true

# grab gosu for easy step-down from root
#RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN arch="$(dpkg --print-architecture)" \
    && set -x \
    && curl --silent -o /usr/local/bin/gosu -fSL "https://github.com/tianon/gosu/releases/download/1.10/gosu-$arch" \
    && EXPECTED_SHA="5b3b03713a888cee84ecbf4582b21ac9fd46c3d935ff2d7ea25dd5055d302d3c" \
    && sha256sum /usr/local/bin/gosu | grep -q $EXPECTED_SHA \
    && chmod +x /usr/local/bin/gosu
#    && curl -o /usr/local/bin/gosu.asc -fSL "https://github.com/tianon/gosu/releases/download/1.10/gosu-$arch.asc" \
#    && gpg --verify /usr/local/bin/gosu.asc \
#    && rm /usr/local/bin/gosu.asc

RUN mkdir -p /app/cache
COPY . /app/
COPY start.bash /start
RUN chown -R u1000:u1000 /app

# compile all pyc in sys.path
RUN python -m compileall
USER u1000
# compile all pyc in in the /app folder
RUN python -m compileall /app
# all the pyc files in the image take 5MB. It's better to have them in the
# image instead of having them generated when the container starts. Think
# about 100 containers started in parallel... less disk write, and we gain
# 495MB of disk space.
WORKDIR /app

RUN mkdir -p -m 700 /app/.ssh && \
    echo "|1|mkhJkTqJT7XEFCg9zJ6vXr9F7KM=|1ihCQCq4xl9SQDtCAqwp4auiRIk= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNn6VI+Ekg/iOz3bZL6bb35tj6fOjmmMOvkw592XDXy+bSes+2qHhcA3uOg5/wEtmRaK583uZH/CJ4512BpLb7M=" >> /app/.ssh/known_hosts && \
    echo "|1|VmfmXO+MNtehwEnpYIEHO7zfvm8=|ya5Yt/ILBv/gMHQLAfSu2tOWO2I= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNn6VI+Ekg/iOz3bZL6bb35tj6fOjmmMOvkw592XDXy+bSes+2qHhcA3uOg5/wEtmRaK583uZH/CJ4512BpLb7M=" >> /app/.ssh/known_hosts
RUN buildout bootstrap -c heroku.cfg
# bin/buildout -c heroku.cfg is done outside this build if do_buildout is false
RUN $run_buildout && bin/buildout -c heroku.cfg || true

USER root

CMD ["/start"]
