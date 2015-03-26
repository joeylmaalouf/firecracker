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
		self.label.set_markup("<span size='"+str(item.text_size*1000)+"'>"+item.text+"</span>")
		self.label.set_justify(gtk.JUSTIFY_CENTER)
		self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(item.text_color))

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.resize(item.w, item.h)
		self.window.move(item.x, item.y)
		self.window.set_title(item.title)
		self.window.set_opacity(item.alpha)
		self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DESKTOP)

		screen = self.window.get_screen()
		rgba = screen.get_rgba_colormap()
		self.window.set_colormap(rgba)
		self.window.set_app_paintable(True)
		self.window.connect("expose-event", self.transparent_expose)
		self.window.connect("key_press_event", self.key_press)

		self.window.add(self.label)
		self.window.set_decorated(False)
		self.window.show_all()

	def update_time(self):
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

