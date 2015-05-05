#!/bin/bash
sudo pip2 install pattern
sudo pip2 install psutil
sudo apt-add-repository -y "deb http://repository.spotify.com stable non-free" && sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 94558F59 && sudo apt-get update -qq && sudo apt-get install spotify-client
echo "cd $(pwd)
./firecracker.py &
cd ~
bash ./bashrc">>~/.gnomerc
echo "Firecracker will now launch on login."
