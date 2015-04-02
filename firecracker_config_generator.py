import sys

import pygtk
pygtk.require("2.0")
import gtk


class MainWindow(gtk.Window):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.connect("destroy", gtk.main_quit)
		self.set_size_request(300, 300)
		self.set_position(gtk.WIN_POS_CENTER)

		self.label = gtk.Label("How many items would you\nlike to have in this skin?")
		self.label.set_justify(gtk.JUSTIFY_CENTER)

		self.counter = gtk.SpinButton()
		self.counter.set_range(0, 99)
		self.counter.set_increments(1, 10)

		self.button = gtk.Button("Go!")
		self.button.connect("button_press_event", self.on_press)

		self.vbox = gtk.VBox()
		self.vbox.pack_start(self.label)
		self.vbox.pack_start(self.counter)
		self.vbox.pack_start(self.button)
		self.add(self.vbox)
		self.show_all()

	def main(self):
		gtk.main()

	def on_press(self, widget, data):
		print(self.counter.get_value_as_int())
		# define a new itemwindow class, and spawn n many of them? somehow combine all of those results?
		# OR: just have this one window, and change the button to append the current properties to a config file
		# (add file path as a field to fill), and clear the fields each time they press the button
		# so they can fill in new values for the next item (make sure to display a label at the top telling them
		# that the item has been successfully appended and that now they're doing a new item)


def main(argv):
	win = MainWindow()
	win.main()


if __name__ == "__main__":
	main(sys.argv)
