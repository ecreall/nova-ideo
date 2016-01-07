#!/bin/bash
rm -rf /app/cache/eggs
rm -rf /app/cache/src
cp -rf /app/eggs /app/cache/
cp -rf /app/src /app/cache/
exec /start
