import cairo
import subprocess
from datetime import datetime
from json import loads
from pattern.web import URL
from firecracker_config_generator import MainWindow

import pygtk
pygtk.require("2.0")
import gtk


class FCManager(object):
	""" The Firecracker Manager object,
		which watches multiple FCWindows.
	"""
	def __init__(self):
		self.num_windows = 0

	def watch(self, window):
		self.num_windows += 1
		window.watcher = self


class FCWindow(object):
	""" The Firecracker Window object, representing
		a user-created customizable display.
	"""
	def __init__(self, item):
		self.vals = item
		self.watcher = None

		self.label = gtk.Label(item.text)
		self.label.set_angle(item.angle)
		self.label.set_markup("<span face='"+item.font+"' size='"+str(item.text_size*1000)+"'>"+str(item.text)+"</span>")
		self.label.set_justify(gtk.JUSTIFY_CENTER)
		self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(item.text_color))

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.resize(item.w, item.h)
		self.window.move(item.x, item.y)
		self.window.set_title(item.title)
		self.window.set_opacity(item.alpha)
		self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)  # uncomment this to remove the taskbar icon, comment to add it back
		self.window.set_keep_below(True)
		self.window.set_icon_from_file("images/logo.png")
		self.window.stick()

		screen = self.window.get_screen()
		rgba = screen.get_rgba_colormap()
		self.window.set_colormap(rgba)
		self.window.set_app_paintable(True)
		self.window.connect("expose-event", self.transparent_expose)
		self.window.connect("key_press_event", self.key_press)

		self.box = gtk.EventBox()
		self.box.set_visible_window(False)
		self.box.connect("button_press_event", self.onclick)
		self.box.connect("button_release_event", self.onrelease)
		self.box.connect("motion_notify_event", self.mousemove)
		self.box.set_events(gtk.gdk.EXPOSURE_MASK|gtk.gdk.BUTTON_PRESS_MASK)

		if self.vals.type == "IMAGE":
			self.image = gtk.Image()
			pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(item.image, width = item.image_w, height = item.image_h)
			self.image.set_from_pixbuf(pixbuf)
			self.box.add(self.image)
		else:
			self.box.add(self.label)

		self.window.add(self.box)
		self.window.set_decorated(False)
		self.window.show_all()


	def update(self):
		if self.vals.type == "CLOCK":
			time = datetime.now().time()
			time_string = "{0:02d}:{1:02d}:{2:02d}".format(time.hour, time.minute, time.second)
			self.label.set_markup("<span face='"+self.vals.font+"' size='"+str(self.vals.text_size*1000)+"'>"+time_string+"</span>")

		elif self.vals.type == "WEATHER":
			try:
				data = loads(URL("http://api.openweathermap.org/data/2.5/weather?zip="+self.vals.zip_code+",us").download())
				status = data["weather"][0]["main"].lower()
				# status = {"clouds":"It's cloudy outside.", "clear":"It's clear outside.", "rain":"It's raining outside."}[status]
				temp = (float(data["main"]["temp"])-273.15)*9/5+32
				weather_string =  "Weather: {0}\nTemperature: {1:0.2f} degrees Fahrenheit.".format(status, temp)
			except:
				weather_string = "Could not retrieve\nweather data"
			self.label.set_markup("<span face='"+self.vals.font+"' size='"+str(self.vals.text_size*1000)+"'>"+weather_string+"</span>")

		return True

	def key_press(self, widget, event):
		x, y = self.window.get_position()

		if gtk.gdk.keyval_name(event.keyval) == "Escape":
			self.window.destroy()
			self.watcher.num_windows -= 1
			if self.watcher.num_windows == 0:
				gtk.main_quit()
		elif gtk.gdk.keyval_name(event.keyval) == "m":
			if event.state & gtk.gdk.CONTROL_MASK:
				MainWindow().main()
		elif gtk.gdk.keyval_name(event.keyval) == "Up":
			y -= 5
		elif gtk.gdk.keyval_name(event.keyval) == "Down":
			y += 5
		elif gtk.gdk.keyval_name(event.keyval) == "Left":
			x -= 5
		elif gtk.gdk.keyval_name(event.keyval) == "Right":
			x += 5
		self.window.move(x, y)

	def onclick (self, widget, event):
		if event.type == gtk.gdk.BUTTON_PRESS:
			self.window.drag = True
			self.drag_x = event.x
			self.drag_y = event.y
		elif event.type == gtk.gdk._2BUTTON_PRESS:
			if self.vals.link:
				try:
					subprocess.call([self.vals.process, self.vals.args])
				except:
					subprocess.call(self.vals.process)
		

	def onrelease(self, widget, event):
		self.window.drag = False

	def mousemove(self, widget, event):
		x, y = self.window.get_position()
		self.window.move(x+int(event.x-self.drag_x), y+int(event.y-self.drag_y))

	def transparent_expose(self, widget, event):
		cr = widget.window.cairo_create()
		cr.set_operator(cairo.OPERATOR_CLEAR)
		region = gtk.gdk.region_rectangle(event.area)
		cr.region(region)
		cr.fill()
		return False


class FCItem(object):
	""" The Firecracker Item object, representing
		the custom data format used for storing data
		read in from configuration files.
	"""
	def __init__(self, type_str):
		self.type = type_str
		self.title = "Firecracker"
		self.x = 0
		self.y = 0
		self.w = 1
		self.h = 1
		self.alpha = 1.0
		self.text = ""
		self.text_size = 16
		self.text_color = "#FFFFFF"
		self.font = "Helvetica"
		self.angle = 0
		self.zip_code = "00000"
		self.link = False
		self.update_timer = 1000


def parse(filepath):
	""" The parsing function for reading configuration
		files and creating a list of FCItems from them.
	"""
	datalist = []
	item = None
	in_item = False
	fileobj = open(filepath, "r")

	for i, line in enumerate(fileobj):
		line = line.strip()
		
		if len(line) == 0:
			continue
		
		elif line[0] == "<":
			in_item = True
			item = FCItem(line[1:].strip().upper())
		
		elif line[0] == ">" and item != None:
			datalist.append(item)
			in_item = False
		
		elif "=" in line and in_item:
			(key, val) = [i.strip() for i in line.split("=", 1)]
			key = key.lower()
			if key == "text":
				item.text = val
			elif key == "pos_x":
				item.x = int(val)
				item.x_line = i
			elif key == "pos_y":
				item.y = int(val)
				item.y_line = i
			elif key == "size_w":
				item.w = int(val)
			elif key == "size_h":
				item.h = int(val)
			elif key == "alpha":
				item.alpha = int(val)/100.0
			elif key == "font_size":
				item.text_size = int(val)
			elif key == "font_color":
				item.text_color = val
			elif key == "font":
				item.font = val
			elif key == "angle":
				item.angle = int(val)
			elif key == "zip_code":
				item.zip_code = str(val)
			elif key == "image":
				item.image = val
			elif key == "image_w":
				item.image_w = int(val)
			elif key == "image_h":
				item.image_h = int(val)
			elif key == "update":
				item.update_timer = int(val)
			elif key == "link":
				item.link = True if val.lower() == "true" else False
			elif key == "process":
				item.process = val
			elif key == "args":
				item.args = val

	fileobj.close()
	return datalist