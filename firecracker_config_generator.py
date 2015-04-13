import pygtk
pygtk.require("2.0")
import gtk


class MainWindow(gtk.Window):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.main = gtk.main

		self.connect("destroy", gtk.main_quit)
		self.set_size_request(500, 700)
		self.set_position(gtk.WIN_POS_CENTER)

		self.label_header = gtk.Label("Generate a Firecracker widget!\nYou can add as many as you like, one at a time.")
		self.label_header.set_justify(gtk.JUSTIFY_CENTER)

		self.label_type = gtk.Label("Widget type:")
		self.form_type = gtk.combo_box_new_text()
		for option in ["TEXT", "CLOCK", "WEATHER", "IMAGE"]:
			self.form_type.append_text(option)
		self.form_type.set_active(0)

		self.label_alpha = gtk.Label("Opacity:")
		self.form_alpha = gtk.SpinButton(adjustment = gtk.Adjustment(0.5, 0.0, 1.0, 0.01, 0.1, 0.0), digits = 2)

		self.label_text = gtk.Label("Text:")
		self.form_text = gtk.Entry()
		self.form_text.set_text("Hello World!")

		self.label_color = gtk.Label("Text color:")
		self.form_color = gtk.ColorButton()
		self.form_color.set_color(gtk.gdk.color_parse("#0000FFFF0000"))

		self.label_size = gtk.Label("Text size:")
		self.form_size = gtk.SpinButton(adjustment = gtk.Adjustment(12.0, 2.0, 128.0, 1.0, 10.0, 0.0), digits = 0)

		self.label_font = gtk.Label("Font:")
		self.form_font = gtk.Entry()
		self.form_font.set_text("Sawasdee")

		self.label_update = gtk.Label("Update timer:")
		self.form_update = gtk.SpinButton(adjustment = gtk.Adjustment(1.0, 0.1, 60.0, 0.1, 1.0, 0.0), digits = 1)

		self.label_angle = gtk.Label("Text angle:")
		self.form_angle = gtk.SpinButton(adjustment = gtk.Adjustment(0.0, 0.0, 359.0, 1.0, 10.0, 0.0), digits = 0)

		self.label_link =  gtk.Label("Clickable link:")
		self.form_link = gtk.combo_box_new_text()
		for option in ["true", "false"]:
			self.form_link.append_text(option)
		self.form_link.set_active(1)

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
		self.table.attach(self.label_font, 0, 1, 6, 7)
		self.table.attach(self.form_font, 1, 2, 6, 7)
		self.table.attach(self.label_update, 0, 1, 7, 8)
		self.table.attach(self.form_update, 1, 2, 7, 8)
		self.table.attach(self.label_angle, 0, 1, 8, 9)
		self.table.attach(self.form_angle, 1, 2, 8, 9)
		self.table.attach(self.label_link, 0, 1, 9, 10)
		self.table.attach(self.form_link, 1, 2, 9, 10)
		self.table.attach(self.button_go, 0, 2, 10, 11, xpadding = 40, ypadding = 25)
		self.table.attach(self.button_quit, 0, 2, 11, 12, xpadding = 40, ypadding = 25)
		self.add(self.table)
		self.show_all()

	def on_press(self, widget, data):
		widget_type = self.form_type.get_active_text()
		string = "< "+widget_type+"\n"
		string += "alpha = "+str(int(100*self.form_alpha.get_value()))+"\n"
		if widget_type == "TEXT":
			string += "text = "+self.form_text.get_text()+"\n"
		if widget_type == "TEXT" or widget_type == "CLOCK":
			string += "font_color = "+self.form_color.get_color().to_string()+"\n"
			string += "font_size = "+str(self.form_size.get_value_as_int())+"\n"
			string += "font = "+self.form_font.get_text()+"\n"
		string += "update_timer = "+str(100*int(10*self.form_update.get_value()))+"\n"
		string += "angle = "+str(self.form_angle.get_value_as_int())+"\n"
		string += "is_link = "+self.form_link.get_active_text()+"\n"
		if self.form_link.get_active_text() == "true":
			pass
			# string += self.form_process
			# string += self.form_args (optiona)
		string += ">"+"\n"
		print(string)  # change this to write to file
		# just have this one window, and change the button to append the current properties to a config file
		# (add file path as a field to fill)
		self.label_header.set_text("Widget added successfully!\nYou may now add another.")


if __name__ == "__main__":
	win = MainWindow()
	win.main()
