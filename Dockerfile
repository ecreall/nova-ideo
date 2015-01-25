FROM progrium/buildstep
MAINTAINER Vincent Fretin <vincentfretin@ecreall.com>

RUN mkdir /app
COPY . /app/
RUN mkdir -p /tmp/env && echo heroku.cfg >/tmp/env/BUILDOUT_CFG
RUN /build/builder

EXPOSE 5000

CMD ["/start", "web"]
