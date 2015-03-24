import pygtk
pygtk.require("2.0")
import gtk


class Window(object):
	def __init__(self, text = "", width = 400, height = 200, xpos = 0, ypos = 0, color = "FFFFFF", alpha = 0.5):
		self.text = gtk.Label(text)
		self.text.set_justify(gtk.JUSTIFY_CENTER)
		self.text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#"+color))

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.resize(width, height)
		self.window.move(xpos, ypos)
		self.window.set_title("")
		self.window.set_opacity(alpha)

		self.window.add(self.text)
		self.window.show_all()


if __name__ == "__main__":
	Window("hello", 400, 200, 100, 300, "00FF00", 1.00)
	Window("world", 200, 400, 300, 100, "FF0000", 0.75)
	gtk.main()
