import sys

import pygtk
pygtk.require("2.0")
import gtk


class MainWindow(gtk.Window):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.connect("destroy", gtk.main_quit)
		self.set_size_request(400, 600)
		self.set_position(gtk.WIN_POS_CENTER)

		self.label_header = gtk.Label("Generate a Firecracker widget!")

		self.label_type = gtk.Label("Widget type:")
		self.form_type = gtk.combo_box_new_text()
		for option in ["TEXT", "CLOCK", "WEATHER", "IMAGE"]:
			self.form_type.append_text(option)
		self.form_type.set_active(0)

		self.label_alpha = gtk.Label("Opacity:")
		self.form_alpha = gtk.SpinButton(adjustment = gtk.Adjustment(0.5, 0.0, 1.0, 0.1, 0.1, 0.0), digits = 2)

		self.label_text = gtk.Label("Text:")
		self.form_text = gtk.Entry()
		self.form_text.set_text("Hello World!")

		self.label_color = gtk.Label("Text color:")
		self.form_color = gtk.ColorButton()
		self.form_color.set_color(gtk.gdk.color_parse("#0000FFFF0000"))

		self.label_size = gtk.Label("Text size:")
		self.form_size = gtk.SpinButton(adjustment = gtk.Adjustment(12.0, 2.0, 128.0, 1.0, 1.0, 0.0), digits = 0)

		self.button_go = gtk.Button("Go!")
		self.button_go.connect("button_press_event", self.on_press)

		self.button_quit = gtk.Button("Exit")
		self.button_quit.connect("button_press_event", gtk.main_quit)

		self.table = gtk.Table()
		self.table.attach(self.label_header, 0, 2, 0, 1)
		self.table.attach(self.label_type, 0, 1, 1, 2)
		self.table.attach(self.form_type, 1, 2, 1, 2)
		self.table.attach(self.label_alpha, 0, 1, 2, 3)
		self.table.attach(self.form_alpha, 1, 2, 2, 3)
		self.table.attach(self.label_text, 0, 1, 3, 4)
		self.table.attach(self.form_text, 1, 2, 3, 4)
		self.table.attach(self.label_color, 0, 1, 4, 5)
		self.table.attach(self.form_color, 1, 2, 4, 5)
		self.table.attach(self.label_size, 0, 1, 5, 6)
		self.table.attach(self.form_size, 1, 2, 5, 6)
		self.table.attach(self.button_go, 0, 2, 6, 7, xpadding = 40, ypadding = 25)
		self.table.attach(self.button_quit, 0, 2, 7, 8, xpadding = 40, ypadding = 25)
		self.add(self.table)
		self.show_all()

	def main(self):
		gtk.main()

	def on_press(self, widget, data):
		string = ""
		string += "< "+self.form_type.get_active_text()+"\n"
		string += "alpha      = "+str(int(100*self.form_alpha.get_value()))+"\n"
		string += "text       = "+self.form_text.get_text()+"\n"
		string += "font_color = "+self.form_color.get_color().to_string()+"\n"
		string += "font_size  = "+str(self.form_size.get_value_as_int())+"\n"
		string += ">"+"\n"
		print(string)
		# just have this one window, and change the button to append the current properties to a config file
		# (add file path as a field to fill), and clear the fields each time they press the button
		# so they can fill in new values for the next item (make sure to display a label at the top telling them
		# that the item has been successfully appended and that now they're doing a new item)
		# e.g. "widget added successfully! you may now add another"


def main(argv):
	win = MainWindow()
	win.main()


if __name__ == "__main__":
	main(sys.argv)
