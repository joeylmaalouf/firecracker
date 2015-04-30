#!/usr/bin/python
from firecracker_utils import FCManager, FCWindow, FCItem, parse_file
import sys

import pygtk
pygtk.require("2.0")
import gtk


def main(argv):
	""" Wrapper for firecracker application. Can be run with specific path to config file or
	with the default config file 'example.cfg'
	"""
	if len(argv) > 2:
		print("Firecracker requires an input of exactly one skin configuration file.")
		return
	elif len(argv) < 2:
		path = "/".join(argv[0].split("/")[:-1])
		if path == "": path = "."
		argv.append(path+"/skins/example.cfg")
		print("\nThis demo uses the provided example configuration.")
		print("You can use your own by typing")
		print("    python2 "+argv[0].split("/")[-1]+" <path to config file>\n")

	config_list = parse_file(argv[1])
	windows = [FCWindow(item) for item in config_list]
	manager = FCManager()
	for window in windows:
		manager.watch(window)
		window.update()
		gtk.timeout_add(window.vals.update_timer, window.update)
	gtk.main()


if __name__ == "__main__":
	main(sys.argv)
