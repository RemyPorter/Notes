import pickle
import os
from collections import defaultdict, namedtuple
from commands import commands

SearchResult = namedtuple("SearchResult", "titles keywords words")
class Index:
	def __init__(self):
		self.__keywords = defaultdict(set)
		self.__words = defaultdict(set)
		self.__titles = set()

	def __add_keywords(self, op):
		keys = op.params
		if keys[0]:
			for k in keys:
				self.__keywords[k].add(op.title)

	def __add_words(self, op):
		words = op.body.split()
		for w in words:
			self.__words[w].add(op.title)

	def __add_title(self, op):
		self.__titles.add(op.title)

	def __stor(self, path):
		return path + ".index.idx"

	def update(self, op):
		if op.command in [commands.add, commands.edit]:
			self.__add_keywords(op)
			self.__add_words(op)
			self.__add_title(op)

	def search(self, op):
		title_match = {}
		keyword_match = {}
		word_match = {}
		if op.title in self.__titles:
			title_match.add(op.title)
		keyword_match = self.__keywords[op.title]
		word_match = self.__words[op.title]
		return SearchResult(title_match, keyword_match, word_match)

	def save(self, repo_path):
		storage = [self.__keywords, self.__words, self.__titles]
		fh = open(self.__stor(repo_path), "wb")
		pickle.dump(storage, fh, protocol=pickle.HIGHEST_PROTOCOL)

	def load(self, repo_path):
		p = self.__stor(repo_path)
		if os.access(p, os.R_OK):
			fh = open(p, "rb")
			storage = pickle.load(fh)
			(self.__keywords, self.__words, self.__titles) = storage

	def dump(self):
		print(self.__keywords, self.__words, self.__titles)