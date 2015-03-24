def parse(filepath):
	type_nums = ["pos_x", "pos_y", "size", "col_r", "col_g", "col_b", "col_a"]

	datalist = []
	in_item = False
	fileobj = open(filepath, "r")

	for line in fileobj:
		line = line.strip()                                     # remove blank space
		
		if len(line) == 0:                                      # skip blank lines
			continue
		
		elif line[0] == "<":                                    # start of item found
			in_item = True
			item = {}                                           # begin parsing for new item
			item["id"] = line[1:].strip()
		
		elif line[0] == ">":                                    # end of item found
			datalist.append(item)                               # add old item
			in_item = False
		
		elif "=" in line and in_item:
			key, val = [i.strip() for i in line.split("=", 1)]  # split into key and value
			if key in type_nums:                                # if necessary,
				val = int(val)                                  # convert to int
			item[key] = val                                     # add the pair to the current item

		else:
			pass                                                # ignore comments

	fileobj.close()
	return datalist


if __name__ == "__main__":
	from pprint import pprint
	pprint(parse("example.cfg"))
