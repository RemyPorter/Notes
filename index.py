import pickle
import os
from collections import defaultdict, namedtuple
from commands import commands

SearchResult = namedtuple("SearchResult", "titles keywords words")
class Index:
	def __init__(self, partial_match=False):
		self.__keywords = defaultdict(set)
		self.__words = defaultdict(set)
		self.__titles = set()
		self.__partial = partial_match

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

	def __full_search(self, op):
		title_match = set()
		keyword_match = set()
		word_match = set()
		if op.title in self.__titles:
			title_match.add(op.title)
		keyword_match = self.__keywords[op.title]
		word_match = self.__words[op.title]
		return SearchResult(title_match, keyword_match, word_match)

	def __partial_search(self, op):
		title_match = set()
		keyword_match = set()
		word_match = set()
		for t in self.__titles:
			if op.title in t:
				title_match.add(t)
		for k in self.__keywords.keys():
			if op.title in k:
				for title in self.__keywords[k]:
					keyword_match.add(title)
		for w in self.__words.keys():
			if op.title in w:
				for title in self.__words[w]:
					word_match.add(title)
		return SearchResult(title_match, keyword_match, word_match)

	def search(self, op):
		if not self.__partial:
			return self.__full_search(op)
		else:
			return self.__partial_search(op)

	def list(self):
		return self.__titles

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