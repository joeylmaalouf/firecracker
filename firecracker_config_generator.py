from firecracker_utils import FCWindow, FCItem, parse_string
from os.path import exists
import time
import pygtk
pygtk.require("2.0")
import gtk


class ConfigWindow(gtk.Window):
	""" This is the selection window, where the
		user chooses which type of widget to add.
	"""
	def __init__(self):
		super(ConfigWindow, self).__init__()
		self.main = gtk.main
		self.quit = gtk.main_quit
		self.connect("destroy", self.quit)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_size_request(400, 400)
		self.set_title("Firecracker Editor")

		self.table = gtk.Table()
		self.buttons = {}
		for i, s in enumerate(["Text", "Clock", "Weather", "Image", "Performance", "Spotify"]):
			self.buttons[s] = gtk.Button(s+" Widget")
			self.buttons[s].connect("button_press_event", self.on_press)
			self.table.attach(self.buttons[s], 0, 1, i, i+1)
		self.add(self.table)
		self.show_all()

	def on_press(self, widget, event):
		""" When any of the buttons are pressed,
			create the corresponding widget window.
		"""
		s = widget.get_label()[:-7]
		win = {"Text":TextWW, "Clock":ClockWW, "Weather":WeatherWW, "Image":ImageWW, "Performance":PerformanceWW, "Spotify":SpotifyWW}[s]()
		win.main()


class WidgetWindow(gtk.Window):
	""" This is the base widget class, from
		which the specific widgets inherit.
	"""
	def __init__(self):
		super(WidgetWindow, self).__init__()
		self.main = gtk.main
		self.quit = gtk.main_quit
		self.connect("destroy", self.quit)

		self.table = gtk.Table()
		
		self.label_path = gtk.Label("Configuration file path:")
		self.form_path = gtk.Entry()
		self.form_path.set_text("./skins/example.cfg")

		self.label_pos = gtk.Label("Position")
		self.form_pos_x = gtk.SpinButton(adjustment = gtk.Adjustment(200.0, 0.0, self.get_screen().get_width(), 1.0, 10.0, 0.0), digits = 0)
		self.form_pos_y = gtk.SpinButton(adjustment = gtk.Adjustment(200.0, 0.0, self.get_screen().get_height(), 1.0, 10.0, 0.0), digits = 0)

		self.label_alpha = gtk.Label("Opacity:")
		self.form_alpha = gtk.SpinButton(adjustment = gtk.Adjustment(0.5, 0.0, 1.0, 0.01, 0.1, 0.0), digits = 2)

		self.label_angle = gtk.Label("Angle:")
		self.form_angle = gtk.SpinButton(adjustment = gtk.Adjustment(0.0, 0.0, 359.0, 1.0, 10.0, 0.0), digits = 0)

		self.label_link =  gtk.Label("Runs a process on click:")
		self.form_link = gtk.combo_box_new_text()
		for option in ["true", "false"]:
			self.form_link.append_text(option)
		self.form_link.set_active(0)

		self.label_process = gtk.Label("Linked process:")
		self.form_process = gtk.Entry()
		self.form_process.set_text("firefox")

		self.label_args = gtk.Label("Optional process flags/arguments:")
		self.form_args = gtk.Entry()
		self.form_args.set_text("github.com")

		self.button_preview = gtk.Button("Preview (ESC to close)")
		self.button_preview.connect("button_press_event", self.preview)

		self.button_go = gtk.Button("Create Widget!")
		self.button_go.connect("button_press_event", self.on_press)

	def make_string(self):
		""" To be overridden by the
			specific widget window classes.
		"""
		return ""

	def preview(self, widget, event):
		""" Preview the current settings.
		"""
		win = FCWindow(parse_string(self.make_string().split("\n"))[0])
		win.window.set_keep_above(True)
		win.update()
		gtk.timeout_add(win.vals.update_timer, win.update)

	def on_press(self, widget, event):
		""" Save the window configuration
			to the specified file.
		"""
		path = self.form_path.get_text()
		f = open(path, "a" if exists(path) else "w")
		f.write(self.make_string())
		f.close()
		time.sleep(0.15)
		self.destroy()


class TextWW(WidgetWindow):
	""" This is the text widget creator, where the
		user sets the properties of a text label.
	"""
	def __init__(self):
		super(TextWW, self).__init__()
		self.set_title("Text Widget")

		self.label_text = gtk.Label("Text:")
		self.form_text = gtk.Entry()
		self.form_text.set_text("Hello World!")

		self.label_color = gtk.Label("Text color:")
		self.form_color = gtk.ColorButton()
		self.form_color.set_color(gtk.gdk.color_parse("#0000FFFF0000"))

		self.label_size = gtk.Label("Text size:")
		self.form_size = gtk.SpinButton(adjustment = gtk.Adjustment(12.0, 2.0, 512.0, 1.0, 10.0, 0.0), digits = 0)

		self.label_font = gtk.Label("Font:")
		self.form_font = gtk.Entry()
		self.form_font.set_text("Sawasdee")

		self.table.attach(self.label_path, 0, 2, 0, 1)
		self.table.attach(self.form_path, 2, 4, 0, 1)
		self.table.attach(self.label_pos, 0, 2, 1, 2)
		self.table.attach(self.form_pos_x, 2, 3, 1, 2)
		self.table.attach(self.form_pos_y, 3, 4, 1, 2)
		self.table.attach(self.label_alpha, 0, 2, 2, 3)
		self.table.attach(self.form_alpha, 2, 4, 2, 3)
		self.table.attach(self.label_angle, 0, 2, 3, 4)
		self.table.attach(self.form_angle, 2, 4, 3, 4)
		self.table.attach(self.label_text, 0, 2, 4, 5)
		self.table.attach(self.form_text, 2, 4, 4, 5)
		self.table.attach(self.label_color, 0, 2, 5, 6)
		self.table.attach(self.form_color, 2, 4, 5, 6)
		self.table.attach(self.label_size, 0, 2, 6, 7)
		self.table.attach(self.form_size, 2, 4, 6, 7)
		self.table.attach(self.label_font, 0, 2, 7, 8)
		self.table.attach(self.form_font, 2, 4, 7, 8)
		self.table.attach(self.label_link, 0, 2, 8, 9)
		self.table.attach(self.form_link, 2, 4, 8, 9)
		self.table.attach(self.label_process, 0, 2, 9, 10)
		self.table.attach(self.form_process, 2, 4, 9, 10)
		self.table.attach(self.label_args, 0, 2, 10, 11)
		self.table.attach(self.form_args, 2, 4, 10, 11)
		self.table.attach(self.button_preview, 0, 4, 11, 12)
		self.table.attach(self.button_go, 0, 4, 12, 13)
		self.add(self.table)
		self.show_all()

	def make_string(self):
		string = "< TEXT\n"
		string += "pos_x = "+str(self.form_pos_x.get_value_as_int())+"\n"
		string += "pos_y = "+str(self.form_pos_y.get_value_as_int())+"\n"
		string += "alpha = "+str(int(100*self.form_alpha.get_value()))+"\n"
		string += "angle = "+str(self.form_angle.get_value_as_int())+"\n"
		string += "text = "+self.form_text.get_text()+"\n"
		string += "font_color = "+self.form_color.get_color().to_string()+"\n"
		string += "font_size = "+str(self.form_size.get_value_as_int())+"\n"
		string += "font = "+self.form_font.get_text()+"\n"
		string += "link = "+self.form_link.get_active_text()+"\n"
		if self.form_link.get_active_text() == "true":
			string += "process = "+self.form_process.get_text()+"\n"
			string += "args = "+self.form_args.get_text()+"\n"
		string += ">"+"\n\n"
		return string


class ClockWW(WidgetWindow):
	""" This is the clock widget creator, where the user
		sets the properties of a display of the current time.
	"""
	def __init__(self):
		super(ClockWW, self).__init__()
		self.set_title("Clock Widget")

		self.label_color = gtk.Label("Text color:")
		self.form_color = gtk.ColorButton()
		self.form_color.set_color(gtk.gdk.color_parse("#0000FFFF0000"))

		self.label_size = gtk.Label("Text size:")
		self.form_size = gtk.SpinButton(adjustment = gtk.Adjustment(12.0, 2.0, 512.0, 1.0, 10.0, 0.0), digits = 0)

		self.label_font = gtk.Label("Font:")
		self.form_font = gtk.Entry()
		self.form_font.set_text("Sawasdee")

		self.label_update = gtk.Label("Update timer:")
		self.form_update = gtk.SpinButton(adjustment = gtk.Adjustment(1.0, 0.1, 60.0, 0.1, 1.0, 0.0), digits = 1)

		self.table.attach(self.label_path, 0, 2, 0, 1)
		self.table.attach(self.form_path, 2, 4, 0, 1)
		self.table.attach(self.label_pos, 0, 2, 1, 2)
		self.table.attach(self.form_pos_x, 2, 3, 1, 2)
		self.table.attach(self.form_pos_y, 3, 4, 1, 2)
		self.table.attach(self.label_alpha, 0, 2, 2, 3)
		self.table.attach(self.form_alpha, 2, 4, 2, 3)
		self.table.attach(self.label_angle, 0, 2, 3, 4)
		self.table.attach(self.form_angle, 2, 4, 3, 4)
		self.table.attach(self.label_color, 0, 2, 4, 5)
		self.table.attach(self.form_color, 2, 4, 4, 5)
		self.table.attach(self.label_size, 0, 2, 5, 6)
		self.table.attach(self.form_size, 2, 4, 5, 6)
		self.table.attach(self.label_font, 0, 2, 6, 7)
		self.table.attach(self.form_font, 2, 4, 6, 7)
		self.table.attach(self.label_update, 0, 2, 7, 8)
		self.table.attach(self.form_update, 2, 4, 7, 8)
		self.table.attach(self.label_link, 0, 2, 8, 9)
		self.table.attach(self.form_link, 2, 4, 8, 9)
		self.table.attach(self.label_process, 0, 2, 9, 10)
		self.table.attach(self.form_process, 2, 4, 9, 10)
		self.table.attach(self.label_args, 0, 2, 10, 11)
		self.table.attach(self.form_args, 2, 4, 10, 11)
		self.table.attach(self.button_preview, 0, 4, 11, 12)
		self.table.attach(self.button_go, 0, 4, 12, 13)
		self.add(self.table)
		self.show_all()

	def make_string(self):
		string = "< CLOCK\n"
		string += "pos_x = "+str(self.form_pos_x.get_value_as_int())+"\n"
		string += "pos_y = "+str(self.form_pos_y.get_value_as_int())+"\n"
		string += "alpha = "+str(int(100*self.form_alpha.get_value()))+"\n"
		string += "angle = "+str(self.form_angle.get_value_as_int())+"\n"
		string += "font_color = "+self.form_color.get_color().to_string()+"\n"
		string += "font_size = "+str(self.form_size.get_value_as_int())+"\n"
		string += "font = "+self.form_font.get_text()+"\n"
		string += "update_timer = "+str(100*int(10*self.form_update.get_value()))+"\n"
		string += "link = "+self.form_link.get_active_text()+"\n"
		if self.form_link.get_active_text() == "true":
			string += "process = "+self.form_process.get_text()+"\n"
			string += "args = "+self.form_args.get_text()+"\n"
		string += ">"+"\n\n"
		return string


class WeatherWW(WidgetWindow):
	""" This is the weather widget creator, where the user
		sets the properties of a display of the current
		weather status and temperature.
	"""
	def __init__(self):
		super(WeatherWW, self).__init__()
		self.set_title("Weather Widget")

		self.label_color = gtk.Label("Text color:")
		self.form_color = gtk.ColorButton()
		self.form_color.set_color(gtk.gdk.color_parse("#0000FFFF0000"))

		self.label_size = gtk.Label("Text size:")
		self.form_size = gtk.SpinButton(adjustment = gtk.Adjustment(12.0, 2.0, 512.0, 1.0, 10.0, 0.0), digits = 0)

		self.label_font = gtk.Label("Font:")
		self.form_font = gtk.Entry()
		self.form_font.set_text("Sawasdee")

		self.label_update = gtk.Label("Update timer:")
		self.form_update = gtk.SpinButton(adjustment = gtk.Adjustment(1.0, 0.1, 60.0, 0.1, 1.0, 0.0), digits = 1)

		self.label_zip = gtk.Label("Zip code (for weather):")
		self.form_zip = gtk.Entry()
		self.form_zip.set_text("02492")

		self.table.attach(self.label_path, 0, 2, 0, 1)
		self.table.attach(self.form_path, 2, 4, 0, 1)
		self.table.attach(self.label_pos, 0, 2, 1, 2)
		self.table.attach(self.form_pos_x, 2, 3, 1, 2)
		self.table.attach(self.form_pos_y, 3, 4, 1, 2)
		self.table.attach(self.label_alpha, 0, 2, 2, 3)
		self.table.attach(self.form_alpha, 2, 4, 2, 3)
		self.table.attach(self.label_angle, 0, 2, 3, 4)
		self.table.attach(self.form_angle, 2, 4, 3, 4)
		self.table.attach(self.label_color, 0, 2, 4, 5)
		self.table.attach(self.form_color, 2, 4, 4, 5)
		self.table.attach(self.label_size, 0, 2, 5, 6)
		self.table.attach(self.form_size, 2, 4, 5, 6)
		self.table.attach(self.label_font, 0, 2, 6, 7)
		self.table.attach(self.form_font, 2, 4, 6, 7)
		self.table.attach(self.label_update, 0, 2, 7, 8)
		self.table.attach(self.form_update, 2, 4, 7, 8)
		self.table.attach(self.label_zip, 0, 2, 8, 9)
		self.table.attach(self.form_zip, 2, 4, 8, 9)
		self.table.attach(self.label_link, 0, 2, 9, 10)
		self.table.attach(self.form_link, 2, 4, 9, 10)
		self.table.attach(self.label_process, 0, 2, 10, 11)
		self.table.attach(self.form_process, 2, 4, 10, 11)
		self.table.attach(self.label_args, 0, 2, 11, 12)
		self.table.attach(self.form_args, 2, 4, 11, 12)
		self.table.attach(self.button_preview, 0, 4, 12, 13)
		self.table.attach(self.button_go, 0, 4, 13, 14)
		self.add(self.table)
		self.show_all()

	def make_string(self):
		string = "< WEATHER\n"
		string += "pos_x = "+str(self.form_pos_x.get_value_as_int())+"\n"
		string += "pos_y = "+str(self.form_pos_y.get_value_as_int())+"\n"
		string += "alpha = "+str(int(100*self.form_alpha.get_value()))+"\n"
		string += "angle = "+str(self.form_angle.get_value_as_int())+"\n"
		string += "font_color = "+self.form_color.get_color().to_string()+"\n"
		string += "font_size = "+str(self.form_size.get_value_as_int())+"\n"
		string += "font = "+self.form_font.get_text()+"\n"
		string += "update_timer = "+str(100*int(10*self.form_update.get_value()))+"\n"
		string += "zip_code = "+self.form_zip.get_text()+"\n"
		string += "link = "+self.form_link.get_active_text()+"\n"
		if self.form_link.get_active_text() == "true":
			string += "process = "+self.form_process.get_text()+"\n"
			string += "args = "+self.form_args.get_text()+"\n"
		string += ">"+"\n\n"
		return string


class ImageWW(WidgetWindow):
	""" This is the image widget creator, where the
		user sets the properties of an image display.
	"""
	def __init__(self):
		super(ImageWW, self).__init__()
		self.set_title("Image Widget")

		self.label_img = gtk.Label("Image file path:")
		self.form_img = gtk.Entry()
		self.form_img.set_text("./images/logo.png")

		self.label_imgs = gtk.Label("Image display size:")
		self.form_imgs_w = gtk.SpinButton(adjustment = gtk.Adjustment(100.0, 0.0, self.get_screen().get_width(), 1.0, 10.0, 0.0), digits = 0)
		self.form_imgs_h = gtk.SpinButton(adjustment = gtk.Adjustment(100.0, 0.0, self.get_screen().get_height(), 1.0, 10.0, 0.0), digits = 0)

		self.table.attach(self.label_path, 0, 2, 0, 1)
		self.table.attach(self.form_path, 2, 4, 0, 1)
		self.table.attach(self.label_pos, 0, 2, 1, 2)
		self.table.attach(self.form_pos_x, 2, 3, 1, 2)
		self.table.attach(self.form_pos_y, 3, 4, 1, 2)
		self.table.attach(self.label_alpha, 0, 2, 2, 3)
		self.table.attach(self.form_alpha, 2, 4, 2, 3)
		self.table.attach(self.label_img, 0, 2, 3, 4)
		self.table.attach(self.form_img, 2, 4, 3, 4)
		self.table.attach(self.label_imgs, 0, 2, 4, 5)
		self.table.attach(self.form_imgs_w, 2, 3, 4, 5)
		self.table.attach(self.form_imgs_h, 3, 4, 4, 5)
		self.table.attach(self.label_link, 0, 2, 5, 6)
		self.table.attach(self.form_link, 2, 4, 5, 6)
		self.table.attach(self.label_process, 0, 2, 6, 7)
		self.table.attach(self.form_process, 2, 4, 6, 7)
		self.table.attach(self.label_args, 0, 2, 7, 8)
		self.table.attach(self.form_args, 2, 4, 7, 8)
		self.table.attach(self.button_preview, 0, 4, 8, 9)
		self.table.attach(self.button_go, 0, 4, 9, 10)
		self.add(self.table)
		self.show_all()

	def make_string(self):
		string = "< IMAGE\n"
		string += "pos_x = "+str(self.form_pos_x.get_value_as_int())+"\n"
		string += "pos_y = "+str(self.form_pos_y.get_value_as_int())+"\n"
		string += "alpha = "+str(int(100*self.form_alpha.get_value()))+"\n"
		string += "image = "+self.form_img.get_text()+"\n"
		string += "image_w = "+str(self.form_imgs_w.get_value_as_int())+"\n"
		string += "image_h = "+str(self.form_imgs_h.get_value_as_int())+"\n"
		string += "link = "+self.form_link.get_active_text()+"\n"
		if self.form_link.get_active_text() == "true":
			string += "process = "+self.form_process.get_text()+"\n"
			string += "args = "+self.form_args.get_text()+"\n"
		string += ">"+"\n\n"
		return string


class PerformanceWW(WidgetWindow):
	""" This is the performance widget creator, where the
		user sets the properties of a display of the
		computer's current performance and usage.
	"""
	def __init__(self):
		super(PerformanceWW, self).__init__()
		self.set_title("Performance Widget")

		self.label_color = gtk.Label("Text color:")
		self.form_color = gtk.ColorButton()
		self.form_color.set_color(gtk.gdk.color_parse("#0000FFFF0000"))

		self.label_size = gtk.Label("Text size:")
		self.form_size = gtk.SpinButton(adjustment = gtk.Adjustment(12.0, 2.0, 512.0, 1.0, 10.0, 0.0), digits = 0)

		self.label_font = gtk.Label("Font:")
		self.form_font = gtk.Entry()
		self.form_font.set_text("Sawasdee")

		self.label_update = gtk.Label("Update timer:")
		self.form_update = gtk.SpinButton(adjustment = gtk.Adjustment(1.0, 0.1, 60.0, 0.1, 1.0, 0.0), digits = 1)

		self.table.attach(self.label_path, 0, 2, 0, 1)
		self.table.attach(self.form_path, 2, 4, 0, 1)
		self.table.attach(self.label_pos, 0, 2, 1, 2)
		self.table.attach(self.form_pos_x, 2, 3, 1, 2)
		self.table.attach(self.form_pos_y, 3, 4, 1, 2)
		self.table.attach(self.label_alpha, 0, 2, 2, 3)
		self.table.attach(self.form_alpha, 2, 4, 2, 3)
		self.table.attach(self.label_angle, 0, 2, 3, 4)
		self.table.attach(self.form_angle, 2, 4, 3, 4)
		self.table.attach(self.label_color, 0, 2, 4, 5)
		self.table.attach(self.form_color, 2, 4, 4, 5)
		self.table.attach(self.label_size, 0, 2, 5, 6)
		self.table.attach(self.form_size, 2, 4, 5, 6)
		self.table.attach(self.label_font, 0, 2, 6, 7)
		self.table.attach(self.form_font, 2, 4, 6, 7)
		self.table.attach(self.label_update, 0, 2, 7, 8)
		self.table.attach(self.form_update, 2, 4, 7, 8)
		self.table.attach(self.label_link, 0, 2, 8, 9)
		self.table.attach(self.form_link, 2, 4, 8, 9)
		self.table.attach(self.label_process, 0, 2, 9, 10)
		self.table.attach(self.form_process, 2, 4, 9, 10)
		self.table.attach(self.label_args, 0, 2, 10, 11)
		self.table.attach(self.form_args, 2, 4, 10, 11)
		self.table.attach(self.button_preview, 0, 4, 11, 12)
		self.table.attach(self.button_go, 0, 4, 12, 13)
		self.add(self.table)
		self.show_all()

	def make_string(self):
		string = "< PERFORMANCE\n"
		string += "pos_x = "+str(self.form_pos_x.get_value_as_int())+"\n"
		string += "pos_y = "+str(self.form_pos_y.get_value_as_int())+"\n"
		string += "alpha = "+str(int(100*self.form_alpha.get_value()))+"\n"
		string += "angle = "+str(self.form_angle.get_value_as_int())+"\n"
		string += "font_color = "+self.form_color.get_color().to_string()+"\n"
		string += "font_size = "+str(self.form_size.get_value_as_int())+"\n"
		string += "font = "+self.form_font.get_text()+"\n"
		string += "update_timer = "+str(100*int(10*self.form_update.get_value()))+"\n"
		string += "link = "+self.form_link.get_active_text()+"\n"
		if self.form_link.get_active_text() == "true":
			string += "process = "+self.form_process.get_text()+"\n"
			string += "args = "+self.form_args.get_text()+"\n"
		string += ">"+"\n\n"
		return string


class SpotifyWW(WidgetWindow):
	""" This is the Spotify widget creator, where the user
		sets the properties of an audio playback controller.
	"""
	def __init__(self):
		super(SpotifyWW, self).__init__()
		self.set_title("Spotify Widget")

		self.label_color = gtk.Label("Color:")
		self.form_color = gtk.ColorButton()
		self.form_color.set_color(gtk.gdk.color_parse("#0000FFFF0000"))

		self.label_size = gtk.Label("Size:")
		self.form_size = gtk.SpinButton(adjustment = gtk.Adjustment(12.0, 2.0, 512.0, 1.0, 10.0, 0.0), digits = 0)

		self.table.attach(self.label_path, 0, 2, 0, 1)
		self.table.attach(self.form_path, 2, 4, 0, 1)
		self.table.attach(self.label_pos, 0, 2, 1, 2)
		self.table.attach(self.form_pos_x, 2, 3, 1, 2)
		self.table.attach(self.form_pos_y, 3, 4, 1, 2)
		self.table.attach(self.label_alpha, 0, 2, 2, 3)
		self.table.attach(self.form_alpha, 2, 4, 2, 3)
		self.table.attach(self.label_angle, 0, 2, 3, 4)
		self.table.attach(self.form_angle, 2, 4, 3, 4)
		self.table.attach(self.label_color, 0, 2, 4, 5)
		self.table.attach(self.form_color, 2, 4, 4, 5)
		self.table.attach(self.label_size, 0, 2, 5, 6)
		self.table.attach(self.form_size, 2, 4, 5, 6)
		self.table.attach(self.button_preview, 0, 4, 6, 7)
		self.table.attach(self.button_go, 0, 4, 7, 8)
		self.add(self.table)
		self.show_all()

	def make_string(self):
		string = "< PLAYER\n"
		string += "pos_x = "+str(self.form_pos_x.get_value_as_int())+"\n"
		string += "pos_y = "+str(self.form_pos_y.get_value_as_int())+"\n"
		string += "alpha = "+str(int(100*self.form_alpha.get_value()))+"\n"
		string += "angle = "+str(self.form_angle.get_value_as_int())+"\n"
		string += "font_color = "+self.form_color.get_color().to_string()+"\n"
		string += "font_size = "+str(self.form_size.get_value_as_int())+"\n"
		string += "font = "+"Ubuntu"+"\n"
		string += "update_timer = "+str(100*int(10*0.1))+"\n"
		string += ">"+"\n\n"
		return string


if __name__ == "__main__":
	win = ConfigWindow()
	win.main()
