import cairo
import subprocess
import psutil
import time
from datetime import datetime
from json import loads
from pattern.web import URL
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
		""" Add a window to be watched for closing.
		"""
		self.num_windows += 1
		window.watcher = self


class FCWindow(object):
	""" The Firecracker Window object, representing
		a user-created customizable display.
	"""
	def __init__(self, item):
		self.vals = item
		self.watcher = None

		self.label = gtk.Label()
		self.label.set_angle(item.angle)
		if self.vals.type == "PLAYER":
			item.text = "&lt;&lt;  ||  &gt;&gt;"
		self.label.set_markup("<span face='"+item.font+"' size='"+str(item.font_size*1000)+"'>"+str(item.text)+"</span>")
		self.label.set_justify(gtk.JUSTIFY_CENTER)
		self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(item.font_color))

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.resize(item.size_w, item.size_h)
		self.window.move(item.pos_x, item.pos_y)
		self.window.set_title(item.title)
		self.window.set_opacity(item.alpha)
			# Uncomment the below line to remove the taskbar icon; comment it to add the icon back.
		self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
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
		self.box.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.BUTTON_PRESS_MASK)
		
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
		""" On non-static widgets, updates with live information. Clock updates the current time,
			weather makes a web API call, and performance uses psutil to check the current status.
		"""
		if self.vals.type == "CLOCK":
			time = datetime.now().time()
			time_string = "{0:02d}:{1:02d}:{2:02d}".format(time.hour, time.minute, time.second)
			self.label.set_markup("<span face='"+self.vals.font+"' size='"+str(self.vals.font_size*1000)+"'>"+time_string+"</span>")

		elif self.vals.type == "WEATHER":
			try:
				data = loads(URL("http://api.openweathermap.org/data/2.5/weather?zip="+self.vals.zip_code+",us").download())
				status = data["weather"][0]["description"].lower()
				status = {"clouds":"cloudy", "clear":"clear", "rain":"rain"}[status]
				temp = (float(data["main"]["temp"])-273.15)*9/5+32
				weather_string =  "Weather: {0}\nTemperature: {1:0.2f} degrees Fahrenheit.".format(status, temp)
			except:
				weather_string = "Could not retrieve\nweather data."
			self.label.set_markup("<span face='"+self.vals.font+"' size='"+str(self.vals.font_size*1000)+"'>"+weather_string+"</span>")

		elif self.vals.type == "PERFORMANCE":
			cpu_usage = psutil.cpu_percent()
			disk_space = psutil.disk_usage("/").percent
			memory_usage = psutil.virtual_memory().percent
			performance_string = "CPU: {0}% || RAM: {1}% || DISK SPACE: {2}%".format(cpu_usage, memory_usage, disk_space)
			self.label.set_markup("<span face='"+self.vals.font+"' size='"+str(self.vals.font_size*1000)+"'>"+performance_string+"</span>")
		
		elif self.vals.type == "PLAYER":
			if subprocess.check_output(["./spotify_controller.sh", "playstatus"]) == "Paused\n":
				player_text = "&lt;&lt;  D  &gt;&gt;"
			elif subprocess.check_output(["./spotify_controller.sh", "playstatus"]) == "Playing\n":
				player_text = "&lt;&lt;  ||  &gt;&gt;"
			else:
				player_text = "Cannot connect to Spotify."
			self.label.set_markup("<span face='"+self.vals.font+"' size='"+str(self.vals.font_size*1000)+"'>"+player_text+"</span>")
#			self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.vals.font_color))

		return True

	def key_press(self, widget, event):
		""" Based on the key pressed by the user,
			updates widget location or deletes widget.
		"""
		x, y = self.window.get_position()

		if gtk.gdk.keyval_name(event.keyval) == "Escape":
			self.window.destroy()
			if self.watcher is not None:
				self.watcher.num_windows -= 1
				if self.watcher.num_windows == 0:
					gtk.main_quit()
		elif gtk.gdk.keyval_name(event.keyval) == "m":
			if event.state & gtk.gdk.CONTROL_MASK:
				subprocess.call(["python2", "./firecracker_config_generator.py"])
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
		""" Tracks user clicking and allows for dragging and relocating of windows.
			Also incudes music player widget functionality.
		"""
		if event.type == gtk.gdk.BUTTON_PRESS:
			self.window.drag = True
			self.drag_x = event.x
			self.drag_y = event.y
			if self.vals.type == "PLAYER":
				label_width = self.label.size_request()[0]
				if self.drag_x < (label_width/3.0):
					subprocess.call(["./spotify_controller.sh", "previous"])
				elif self.drag_x > (label_width/3.0+label_width/12.0) and self.drag_x < (2*label_width/3.0-label_width/12.0):
					subprocess.call(["./spotify_controller.sh", "playpause"])
				elif self.drag_x > (2*label_width/3.0):
					subprocess.call(["./spotify_controller.sh", "next"])
		elif event.type == gtk.gdk._2BUTTON_PRESS:
			if self.vals.link:
				try:
					subprocess.call([self.vals.process, self.vals.args, "&"])
				except:
					subprocess.call([self.vals.process, "&"])
		

	def onrelease(self, widget, event):
		""" When click is released, windows can no longer drag.
		"""
		self.window.drag = False

	def mousemove(self, widget, event):
		""" Tracks the moving of the mouse when dragging widgets.
		"""
		x, y = self.window.get_position()
		self.window.move(x+int(event.x-self.drag_x), y+int(event.y-self.drag_y))

	def transparent_expose(self, widget, event):
		""" Uses Cairo to make widgets have transparent windows.
		"""
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
		self.text = ""
		self.pos_x = 0
		self.pos_y = 0
		self.size_w = 1
		self.size_h = 1
		self.alpha = 1.0
		self.font_size = 16
		self.font_color = "#FFFFFF"
		self.font = "Helvetica"
		self.angle = 0
		self.zip_code = "00000"
		self.image = "./images/empty.png"
		self.image_w = -1
		self.image_h = -1
		self.update_timer = 1000
		self.link = False
		self.process = ""
		self.args = ""
		self.sanitizer_map = {	"text"        :str,
								"pos_x"       :int,
								"pos_y"       :int,
								"size_w"      :int,
								"size_h"      :int,
								"alpha"       :lambda x: int(x)/100.0,
								"font_size"   :int,
								"font_color"  :str,
								"font"        :str,
								"angle"       :int,
								"zip_code"    :str,
								"image"       :str,
								"image_w"     :int,
								"image_h"     :int,
								"update_timer":int,
								"link"        :lambda x: True if x.lower() == "true" else False,
								"process"     :str,
								"args"        :str	}

	def set_attribute(self, key, value):
		""" Sets widget attributes, modifying the values as appropriate.
		"""
		if hasattr(self, key):
			self.__setattr__(key, self.sanitizer_map[key](value))
			return True
		else:
			return False


def parse_file(filepath):
	""" The wrapper for parsing, which allows
		the user to specify a filepath instead
		of a list of lines.
	"""
	fileobj = open(filepath, "r")
	linelist = fileobj.readlines()
	fileobj.close()
	return parse_string(linelist)


def parse_string(linelist):
	""" The parsing function for reading configuration
		settings and creating a list of FCItems from them.
	"""
	datalist = []
	item = None
	in_item = False

	for line in linelist:
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
			item.set_attribute(key, val)

	return datalist
