#!/bin/bash
sudo pip2 install pattern
sudo pip2 install psutil
echo "cd $(pwd)
./firecracker.py &
cd ~
bash ./bashrc">>~/.gnomerc
echo "Firecracker will now launch on login."
