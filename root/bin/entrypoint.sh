#!/bin/sh
set -e

mkdir -p /var/log/simple_app

exec /usr/bin/supervisord -c /etc/supervisord.conf
