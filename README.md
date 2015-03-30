# firecracker

[View the website here.](http://joeylmaalouf.github.io/firecracker/)


### What is it?

Rainmeter for Ubuntu, done in Python.

Firecracker is a fanmade rewrite of Rainmeter for Ubuntu. Just like Rainmeter, Firecracker windows are fully customizable through editing of configuration files, giving users the ability to tweak and edit their windows to their liking.


### Why?

This is our final project for SoftDes Spring 2015 at Olin.


### Dependencies
PyGTK

(comes with Ubuntu)

Pyglet

`sudo pip2 install pyglet`


### How To Use It

In order to have Firecracker run on startup:

1. clone this repo to some location `.../firecracker`
2. `$ cd .../firecracker`
3. put your configuration in `skins/example.cfg`
4. `$ sudo ./install.sh`
5. restart computer

In order to run Firecracker manually:

`python2 firecracker.py <config file>`


### Notes

If your system does not have both Python 2 and Python 3 installed, you should be able to use `pip` and `python` instead of `pip2` and `python2`.
