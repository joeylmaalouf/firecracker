from util import FCWindow, FCItem, parse

import sys
import pygtk
pygtk.require("2.0")
import gtk


def main(argv):
	if len(argv) < 2:
		argv.append("./example.cfg")

	config_list = parse(argv[1])
	for item in config_list:
		FCWindow(item)
	gtk.main()


if __name__ == "__main__":
	main(sys.argv)
