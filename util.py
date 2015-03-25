import pygtk
pygtk.require("2.0")
import gtk


class FCWindow(object):
	""" The Firecracker Window object, representing
		a user-created customizable display.
	"""
	def __init__(self, item):
		self.label = gtk.Label(item.text)
		self.label.set_markup("<span size='"+str(item.text_size*1000)+"'>"+item.text+"</span>")
		self.label.set_justify(gtk.JUSTIFY_CENTER)
		self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(item.text_color))

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.resize(item.w, item.h)
		self.window.move(item.x, item.y)
		self.window.set_title(item.title)
		self.window.set_opacity(item.alpha)
		self.window.connect("key_press_event", self.key_press)

		self.window.add(self.label)
		self.window.show_all()
		self.window.get_window().set_decorations(gtk.gdk.DECOR_BORDER)

	def key_press(self, widget, event):
		if gtk.gdk.keyval_name(event.keyval) == "Escape":
			gtk.main_quit()

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
			item = FCItem(line[1:].strip())
		
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

	fileobj.close()
	return datalist
