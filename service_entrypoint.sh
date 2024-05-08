#!/bin/bash

sleep 10
# Do not muck with Database
# flask db migrate
# flask db upgrade

which gunicorn
which waitress-serve

# waitress-serve --host 127.0.0.1 pdqs.app:app

tail -f /dev/null
