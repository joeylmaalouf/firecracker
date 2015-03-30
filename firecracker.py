from utils import FCWindow, FCItem, parse
import sys

import pygtk
pygtk.require("2.0")
import gtk


def main(argv):
	if len(argv) == 1:
		argv.append("./skins/example.cfg")
		print("\nThis demo uses the provided example configuration.")
		print("You can use your own by typing")
		print("    python2 "+argv[0].split("/skins/")[-1]+" <config file>\n")
	else:
		print("Firecracker requires an input of exactly one skin configuration file.")
		return

	config_list = parse(argv[1])
	windows = [FCWindow(item) for item in config_list]
	for window in windows:
		gtk.timeout_add(window.vals.update_timer, window.update)
	gtk.main()


if __name__ == "__main__":
	main(sys.argv)

# to do:
# make sure to do gtk.main_quit() after the last window closes so everything actually ends
# also, enable movement with click and drag anywhere on the window
# also, add text rotation angle to config files
# maybe have meter type (TEXT, CLOCK, WEATHER, IMAGE, etc.) where ID was?
