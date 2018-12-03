#!./venv/bin/python
import sys
import subprocess

command = ['./venv/bin/node', './solidarity/static/node_modules/.bin/prettier-eslint'] + sys.argv[1:]
p = subprocess.Popen(command, stderr=subprocess.PIPE)
error = p.communicate()[1]

if p.returncode != 0:
    sys.exit(p.returncode)

if b'success' in error:
    sys.exit(1)

sys.exit(0)
