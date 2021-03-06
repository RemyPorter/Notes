import os

def indexed(function):
	def wrapper(*args, **kwargs):
		function(*args, **kwargs)
		operation = None
		if "op" in kwargs.keys():
			operation = kwargs["op"]
		else:
			operation = args[1]
		args[0].update_idx(operation)
	return wrapper

class NoteManager:
	def __init__(self, repo_path, index=None, versioner=None):
		self.__version = versioner
		self.__repo = repo_path
		self.__fmt = ".md"
		self.__idx = index

	def __path(self, title):
		return self.__repo + title + self.__fmt

	def __avoid_dups(self, optitle):
		title = optitle
		count = 1
		while os.access(self.__path(title), os.F_OK):
			title = optitle + str(count)
			count += 1
		return title

	def update_idx(self, op):
		if self.__idx:
			self.__idx.update(op)
			self.__version.commit(op)

	@indexed
	def add(self, op):
		title = self.__avoid_dups(op.title)
		with open(self.__path(title), "w") as note:
			note.write(op.body)

	@indexed
	def delete(self, op):
		try:
			os.remove(self.__path(op.title))
		except Exception as err:
			print(err)

	@indexed
	def edit(self, op):
		try:
			self.delete(op)
			self.add(op)
		except Exception as err:
			print(err)

	def read(self, op):
		if self.__idx:
			matches = self.__idx.search(op)
			if len(matches.titles) > 0:
				fh = open(self.__path(op.title), "r")
				return fh.read()

	def find(self, op):
		if self.__idx:
			return self.__idx.search(op)

	def log(self, op):
		if self.__version:
			self.__version.show_log()

	def undo(self, op):
		if self.__version:
			self.__version.undo(op.params)

	def git(self, op):
		if self.__version:
			self.__version.git(op.params)

	def list(self, op):
		if self.__idx:
			return self.__idx.list()