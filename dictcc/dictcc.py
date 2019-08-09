#!/usr/bin/python3

import requests as __requests__
import os as __os__
import textwrap as __textwrap__

from tabulate import tabulate as __tabulate__
from bs4 import BeautifulSoup as __BeautifulSoup__

class Dictcc:

	def __init__(self):
		_, self.columns          = __os__.popen('stty size', 'r').read().split()
		self.requests_session    = __requests__.Session()
		self.current_suggestions = []

	def __request__(self, word: str, f: str, t: str):
		header  = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:31.0)' +
					' ' + 'Gecko/20100101 Firefox/31.0'}
		payload = {'s': word}
		r = self.requests_session.get(
				"https://{}{}.dict.cc/".format(f, t),
				headers=header,
				params=payload)
		return r.content

	def __parse_single_tag__(self, tag) -> str:
		str_tag = " ".join([a_tag.text for a_tag in tag.find_all('a')])
		if (tag.dfn):
			all_dfn = ", ".join([dfn_tag.text for dfn_tag in tag.find_all('dfn')])
			str_tag = ' '.join([str_tag, '(' + all_dfn + ')'])
		return '\n   '.join(__textwrap__.wrap(str_tag, (int(self.columns) - 8) / 2))

	def __parse_response__(self, html):
		soup        = __BeautifulSoup__(html, 'html.parser')
		data        = [tag for tag in soup.find_all('td', 'td7nl')]
		raw_from_to = zip(data[::2], data[1::2])
		res_from_to = list()
		for f, t in raw_from_to:
			res_from_to.append([self.__parse_single_tag__(f), self.__parse_single_tag__(t)])
		return res_from_to

	def __parse_suggestions__(self, html) -> list:
		soup = __BeautifulSoup__(html, 'html.parser')
		data = [tag.a.text for tag in soup.find_all('td', 'td3nl') if tag.a]
		return data

	def translate(self, word: str, primary_lang: str, secondary_lang: str):
		"""
		Queries dict.cc for word in primary_lang and secondary_lang and
		returns the parsed results and parsed suggestions
		"""
		c = self.__request__(word, primary_lang, secondary_lang)
		return self.__parse_response__(c), self.__parse_suggestions__(c)

	def handle_translation(self, word: str, primary_lang: str, secondary_lang: str) -> None:
		try:
			# if in console mode and a suggestion is chosen by its number,
			# apply the selection
			word = self.current_suggestions[int(word) - 1]
		except (ValueError, IndexError) as e:
			# act like nothing happened. seems like 'word' really was
			# meant to be a word
			pass
		data = None
		try:
			result, suggestions = self.translate(word, primary_lang, secondary_lang)
		except Exception as e:
			print("While querying dict.cc, the following error occurred")
			print(e)
			return
		if result:
			print(__tabulate__(result, [primary_lang, secondary_lang], tablefmt='orgtbl'))
			self.current_suggestions = []
		else:
			print(' '.join(["No translation found for:", word]))
			self.current_suggestions = suggestions
			if len(suggestions) > 0:
				print('Suggestions given by dict.cc (choose by entering the number):')
				for i,s in enumerate(suggestions):
					print(" - {}: {}".format(i+1, s))

	def handle_console(self, primary_lang: str, secondary_lang: str) -> None:
		print('Enter a word for translation')
		print('Enter q or hit CTRL+C for exit')
		try:
			user_input = None
			while user_input != 'q':
				user_input = input('> ')
				self.handle_translation(user_input, primary_lang, secondary_lang)
		except KeyboardInterrupt:
			return
