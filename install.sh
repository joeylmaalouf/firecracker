#!/bin/bash
cwd=`pwd`
echo "start on runlevel [5]
stop on runlevel [!5]
exec $cwd/firecracker.py" > /etc/init/firecracker_startup.conf
