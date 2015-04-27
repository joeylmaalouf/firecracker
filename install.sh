#!/bin/bash
echo "cd $(pwd)
./firecracker.py &
cd ~
bash ./bashrc">>~/.gnomerc
