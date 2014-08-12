import sh
import os
from commands import commands

def dirvert(function):
	def wrapper(*args, **kwargs):
		self = args[0]
		os.chdir(self.dir)
		function(*args, **kwargs)
		os.chdir(self.cwd)
	return wrapper

class Git:
	def __init__(self, notedir):
		self.cwd = os.getcwd()
		self.dir = notedir
		self.init_repo(self.dir)

	def __ignores(self):
		with open(".gitignore", "w") as ignore:
			ignore.write(".gitignore\n")
			ignore.write(".index.idx\n")

	@dirvert
	def init_repo(self, dir):
		if os.access(dir + ".git", os.F_OK):
			return
		else:
			sh.git("init")
			self.__ignores()
			sh.touch("SampleNote.md")
			sh.git("add", "*.md")
			sh.git("commit", "-a", m="Initial create.")
		
	def opstring(self, op):
		return "{0.command}: {0.title} with body {0.body} {0.params}".format(op)	

	@dirvert
	def commit(self, op):
		if op.command == commands.add:
			sh.git("add", op.title + "*.md")
		if op.command == commands.delete:
			sh.git("remove", op.title + ".md")
		sh.git("commit", "-a", m=self.opstring(op))

	@dirvert
	def show_log(self):
		print(sh.git("log"))

	@dirvert
	def undo(self, changes):
		reverts = " ".join(changes)
		sh.git("revert", "--no-edit","-n", changes)
		sh.git("commit", "-a", m="Reverted: {0}".format(changes))

