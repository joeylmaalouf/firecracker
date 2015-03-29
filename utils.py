import pygtk
pygtk.require("2.0")
import gtk

import cairo
from datetime import datetime


class FCWindow(object):
	""" The Firecracker Window object, representing
		a user-created customizable display.
	"""
	def __init__(self, item):
		self.vals = item

		self.label = gtk.Label(item.text)
		self.label.set_markup("<span face='"+item.font+"' size='"+str(item.text_size*1000)+"'>"+str(item.text)+"</span>")
		self.label.set_justify(gtk.JUSTIFY_CENTER)
		self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(item.text_color))

		# file_name = "images/logoWeb.png"
		# pixbuf = gtk.gdk.pixbuf_new_from_file(file_name)
		# pixmap, mask = pixbuf.render_pixmap_and_mask()
		# self.image = gtk.Image()
		# self.image.set_from_pixmap(pixmap, mask)

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.resize(item.w, item.h)
		self.window.move(item.x, item.y)
		self.window.set_title(item.title)
		self.window.set_opacity(item.alpha)
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

		#self.window.add(self.image)
		self.window.add(self.label)
		self.window.set_decorated(False)
		self.window.show_all()

	def update(self):
		if self.vals.clock:
			time = datetime.now().time()
			time_string = "{0:02d}:{1:02d}:{2:02d}".format(time.hour, time.minute, time.second)
			self.label.set_markup("<span size='"+str(self.vals.text_size*1000)+"'>"+time_string+"</span>")
		return True

	def key_press(self, widget, event):
		if gtk.gdk.keyval_name(event.keyval) == "Escape":
			gtk.main_quit()

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
	def __init__(self, id_str):
		self.title = id_str
		self.x = 0
		self.y = 0
		self.w = 400
		self.h = 200
		self.alpha = 1.0
		self.text = ""
		self.text_color = "#FFFFFF"
		self.text_size = 16
		self.font = "Helvetica"
		self.update_timer = 1000
		self.clock = False


	def __str__(self):
		return ("Title: "+self.title+"\n"+
		"Position: "+str(self.x)+", "+str(self.y)+"\n"+
		"Size: "+str(self.w)+", "+str(self.h)+"\n"+
		"Transparency: "+str(self.alpha)+"\n"+
		"Text: "+self.text+"\n"+
		"Text Color: "+self.text_color+"\n"+
		"Text Size: "+str(self.text_size)+"\n"+
		"Font: "+self.font+"\n"+
		"Clock: "+str(self.clock)+"\n"+
		"Update timer: "+str(self.update_timer))


def parse(filepath):
	""" The parsing function for reading configuration
		files and creating a list of FCItems from them.
	"""
	datalist = []
	in_item = False
	fileobj = open(filepath, "r")

	for line in fileobj:
		line = line.strip()
		
		if len(line) == 0:
			continue
		
		elif line[0] == "<":
			in_item = True
			item = FCItem('FireCracker')
		
		elif line[0] == ">":
			datalist.append(item)
			in_item = False
		
		elif "=" in line and in_item:
			key, val = [i.strip() for i in line.split("=", 1)]
			if key == "text":
				item.text = val
			elif key == "pos_x":
				item.x = int(val)
			elif key == "pos_y":
				item.y = int(val)
			elif key == "size_w":
				item.w = int(val)
			elif key == "size_h":
				item.h = int(val)
			elif key == "alpha":
				item.alpha = int(val)/100.
			elif key == "font_size":
				item.text_size = int(val)
			elif key == "font_color":
				item.text_color = "#"+val
			elif key == "font":
				item.font = val
			elif key == "clock" and val.lower() == "true":
				item.clock = True
			elif key == "update":
				item.update_timer = int(val)

	fileobj.close()
	return datalist
