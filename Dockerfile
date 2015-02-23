FROM progrium/buildstep
MAINTAINER Vincent Fretin <vincentfretin@ecreall.com>

RUN mkdir -p /app
COPY . /app/
RUN mkdir -p /tmp/env && echo heroku.cfg >/tmp/env/BUILDOUT_CFG
RUN /build/builder

EXPOSE 5000
VOLUME /app/var

CMD ["/start", "web"]
