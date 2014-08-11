#!/usr/bin/env python3

import os
import os.path
import shutil
from sh import git
from optparse import OptionParser
import collections
from operations import NoteManager
import notedir
from commands import commands, Op
import index
import output

def build_CLI():
	parser = OptionParser()
	parser.add_option("-d", "--dir", dest="repo_dir", help="Set the directory to use for finding/reading/managing notes.", default="~/.notes")
	parser.add_option("-p", "--partial", action="store_true", dest="partial_match", help="Allow partial matching on title to find notes", default=False)
	parser.add_option("-c", "--cleanout", action="store_true", dest="clean_out", help="Clear the active repo entirely. DESTROYS ALL NOTES.", default=False)
	parser.add_option("-m", "--html", action="store_true", dest="markdown", help="Used with read. Outputs in HTML, after markdown processing.", default=False)
	#todo: this needs some features to help manage git history, because this is going to use a git repo
	return parser

def parse_commands(cmds, parser):
	try:
		if not cmds[0] in commands:
			raise ValueError
		operation = None
		if cmds[0] in [commands.add, commands.edit]:
			if (len(cmds) == 3):
				cmds += [None]
			operation = Op(cmds[0], cmds[1], cmds[2], cmds[3:])
		else:
			operation = Op(cmds[0], cmds[1], None, cmds[2:])
		return operation
	except (IndexError, ValueError) as err:
		parser.print_usage()

def main():
	parser = build_CLI()
	(options, arguments) = parser.parse_args()
	cmds = parse_commands(arguments, parser)
	if options.repo_dir[-1] != "/":
		options.repo_dir += "/"
	options.repo_dir = os.path.expanduser(options.repo_dir)
	if (options.clean_out):
		notedir.clean_out(options.repo_dir)
	notedir.check_dir(options.repo_dir)

	idx = index.Index()
	idx.load(options.repo_dir)

	mgr = NoteManager(options.repo_dir, idx)
	res = eval("mgr.{0}(cmds)".format(cmds.command))

	if res and options.markdown and cmds.command == commands.read:
		output.mdown(res)
	elif res:
		output.output(res)

	idx.save(options.repo_dir)

main()