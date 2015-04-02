import sys

import pygtk
pygtk.require("2.0")
import gtk


class PyWindow(gtk.Window):
	def __init__(self):
		super(PyWindow, self).__init__()
		self.connect("destroy", gtk.main_quit)
		self.set_size_request(400, 400)
		self.set_position(gtk.WIN_POS_CENTER)
		self.show()

	def main(self):
		gtk.main()


def main(argv):
	win = PyWindow()
	win.main()


if __name__ == "__main__":
	main(sys.argv)
