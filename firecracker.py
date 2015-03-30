from multiprocessing import Process, Value
from utils import FCWindow, FCItem, parse
import sys

import pygtk
pygtk.require("2.0")
import gtk


def check_done(n):
	while True:
		if n == 0:
			gtk.main_quit()
			sys.exit()


def main(argv):
	if len(argv) == 1:
		argv.append("./skins/example.cfg")
		print("\nThis demo uses the provided example configuration.")
		print("You can use your own by typing")
		print("    python2 "+argv[0].split("/")[-1]+" <config file>\n")
	else:
		print("Firecracker requires an input of exactly one skin configuration file.")
		return

	config_list = parse(argv[1])
	windows = [FCWindow(item) for item in config_list]
	for window in windows:
		gtk.timeout_add(window.vals.update_timer, window.update)

	# run multiple processes concurrently to check for when to end everything
	num_windows = Value("i", len(windows))
	window_process = Process(target = gtk.main)
	manager_process = Process(target = check_done, args = (num_windows,))
	window_process.start()
	manager_process.start()
	window_process.join()
	manager_process.join()


if __name__ == "__main__":
	main(sys.argv)

# to do:
# enable movement with click and drag anywhere on the window
# add text rotation angle to config files
