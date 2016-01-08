#!/bin/bash
rm -rf /app/cache/eggs
rm -rf /app/cache/src
# tests directory have permission issue, I don't understand why
rm -rf /app/eggs/Chameleon-*.egg/chameleon/tests/
cp -rf /app/eggs /app/cache/
cp -rf /app/src /app/cache/
exec /start
