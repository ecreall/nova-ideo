#!/bin/bash
set -e

options=${options:-"-f docker-compose-dev.yml"}

do_buildout() {
    CACHE_PATH=${CACHE_PATH:-$PWD/cache}
    IMAGE=${IMAGE:-"novaideo_novaideo:latest"}
    # do the buildout
    if [ ! -z "$SSH_AUTH_SOCK" ]; then
        id=$(docker run -d -v $CACHE_PATH:/app/cache -v $SSH_AUTH_SOCK:/app/cache/auth.sock -e SSH_AUTH_SOCK=/app/cache/auth.sock -u u1000 $IMAGE ./bin/buildout -c heroku.cfg)
    else
        id=$(docker run -d -v $CACHE_PATH:/app/cache -v /tmp/deploy_id_rsa:/app/.ssh/id_rsa -u u1000 $IMAGE ./bin/buildout -c heroku.cfg)
    fi
    docker attach "$id"
    test "$(docker wait "$id")" -eq 0
    docker commit "$id" "$IMAGE" > /dev/null
    # some files in cache/eggs/Chameleon-2.22-py3.4.egg/chameleon/tests/inputs/ are only readable by u1000, remove them
    # else you can't do the tar from outside
    docker run --rm -v $CACHE_PATH:/app/cache -u u1000 $IMAGE rm -rf /app/cache/eggs/Chameleon-2.22-py3.4.egg/chameleon/tests
    # copy cache in docker image
    id=$(cd $CACHE_PATH/.. && tar -c cache | docker run -i -a stdin -u u1000 "$IMAGE" /bin/bash -c "mkdir -p /app/cache && tar -xC /app")
    test "$(docker wait "$id")" -eq 0
    docker commit --change 'USER root' --change='CMD ["/start"]' "$id" "$IMAGE"
}

case "$1" in
  rebuild)
    mkdir -p cache
    chmod o+rwx cache
    docker-compose $options pull
    docker-compose $options build --pull
    do_buildout
    ;;
  buildout)
    do_buildout
    ;;
  *)
    if [ -z "$1" ]; then
      docker-compose $options up -d
      docker attach novaideo_novaideo_1
    else
      docker-compose $options $@
    fi
   ;;
esac
