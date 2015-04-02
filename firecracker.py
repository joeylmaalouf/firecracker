from firecracker_utils import FCManager, FCWindow, FCItem, parse
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
	elif len(argv) > 2:
		print("Firecracker requires an input of exactly one skin configuration file.")
		return

	config_list = parse(argv[1])
	windows = [FCWindow(item) for item in config_list]
	manager = FCManager()
	for window in windows:
		manager.watch(window)
		gtk.timeout_add(window.vals.update_timer, window.update)
		window.update()
	gtk.main()


if __name__ == "__main__":
	main(sys.argv)

# todo:
# config file generator
# fix install.sh
