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
		self.clock = False

	def __str__(self):
		return ("Title: "+self.title+"\n"+
		"Position: "+str(self.x)+", "+str(self.y)+"\n"+
		"Size: "+str(self.w)+", "+str(self.h)+"\n"+
		"Transparency: "+str(self.alpha)+"\n"+
		"Text: "+self.text+"\n"+
		"Text Color: "+self.text_color+"\n"+
		"Text Size: "+str(self.text_size)+"\n"+
		"Clock: "+str(self.clock))


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
			elif key == "clock" and val.lower() == "true":
				item.clock = True

	fileobj.close()
	return datalist
