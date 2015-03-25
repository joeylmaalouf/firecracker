# firecracker


### What is it?

Rainmeter for Ubuntu, done in Python.

Just like Rainmeter, Firecracker windows are fully customizable through editing of configuration files.


### Why?

This is our final project for SoftDes Spring 2015 at Olin.


### Dependencies
PyGTK

(comes with Ubuntu)

Pyglet

`sudo pip2 install pyglet`


GLUT (OpenGL Utility Toolkit), and all the variations thereof.

```
sudo apt-get install ...
... freeglut3
... freeglut3-dev
... libglew1.5
... libglew1.5-dev
... libglu1-mesa
... libglu1-mesa-dev
... libgl1-mesa-glx
... libgl1-mesa-dev
```


### How To Use It

`python2 firecracker.py <config file>`


### Notes

If your system does not have both Python 2 and Python 3 installed, you should be able to use `pip` and `python` instead of `pip2` and `python2`.
