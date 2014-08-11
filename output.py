def __write(data):
	print(data)

def __write_key(tag, data):
	print(tag + ":")
	if len(data) == 0:
		print("\tNo Results")
	for i in data:
		print("\t" + i)

def __write_results(data):
	__write_key("Titles", data.titles)
	__write_key("Keywords", data.keywords)
	__write_key("Contains word", data.words)

def output(data):
	if type(data).__name__ != 'SearchResult':
		__write(data)
	else:
		__write_results(data)