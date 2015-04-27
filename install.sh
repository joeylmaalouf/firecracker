#!/bin/bash

cwd=`pwd`

echo "start on runlevel [2345]
stop on runlevel [!2345]
exec $cwd/firecracker.py" > /etc/init/firecracker_startup.conf
