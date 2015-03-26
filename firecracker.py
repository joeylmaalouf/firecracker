from util import FCWindow, FCItem, parse

import pygtk
pygtk.require("2.0")
import gtk

import sys


def main(argv):
	if len(argv) < 2:
		argv.append("./example.cfg")
		print("\nThis demo uses the provided example configuration.")
		print("You can use your own by typing")
		print("    python2 "+argv[0].split("/")[-1]+" <config file>\n")

	config_list = parse(argv[1])
	windows = [FCWindow(item) for item in config_list]
	for window in windows:
		if window.vals.clock:
			gtk.timeout_add(1000, window.update_time)
	gtk.main()


if __name__ == "__main__":
	main(sys.argv)

# to do: close windows individually instead of all at once with escape button
# make sure to do gtk.main_quit() after the last one so everything actually closes though
# also, enable movement with click and drag anywhere on the window
