#!/usr/bin/python3

import sys
import requests
import argparse
import os
import textwrap

from tabulate import tabulate
from bs4 import BeautifulSoup

class Dictcc:

	def __init__(self):
		_, self.columns          = os.popen('stty size', 'r').read().split()
		self.requests_session    = requests.Session()
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
		return '\n   '.join(textwrap.wrap(str_tag, (int(self.columns) - 8) / 2))

	def __parse_response__(self, html):
		soup        = BeautifulSoup(html, 'html.parser')
		data        = [tag for tag in soup.find_all('td', 'td7nl')]
		raw_from_to = zip(data[::2], data[1::2])
		res_from_to = list()
		for f, t in raw_from_to:
			res_from_to.append([self.__parse_single_tag__(f), self.__parse_single_tag__(t)])
		return res_from_to

	def __parse_suggestions__(self, html) -> list:
		soup = BeautifulSoup(html, 'html.parser')
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
			print(tabulate(result, [primary_lang, secondary_lang], tablefmt='orgtbl'))
			self.current_suggestions = []
		else:
			print(' '.join(["No translation found for:", word]))
			self.current_suggestions = suggestions

			print('\nSuggestions given by dict.cc'
					+ 'choose by entering the number):')
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

def main():
	prim     = ['de', 'en']
	sec      = ['bg', 'bs', 'cs', 'da', 'el', 'eo', 'es', 'fi', 'fr', 'hr',
				'hu', 'is', 'it', 'la', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sk',
				'sq', 'sr', 'sv', 'tr']
	all_dict = prim + sec
	parser   = argparse.ArgumentParser(
			description='Query dict.cc for a translation.',
			formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-p', '--prim', type=str, default='en', help='Primary language')
	parser.add_argument('-s', '--sec', type=str, default='de', help='Secondary language')
	parser.add_argument('-c', '--console', action='store_true')
	parser.add_argument('word', nargs=argparse.REMAINDER, help='word to translate')

	args = parser.parse_args()

	if not args.prim in prim:
		print("Primary lang must be in : [" + ", ".join(prim) + "]")
		exit(1)
	if not args.sec in all_dict:
		print("Secondary lang must be in : [" + ", ".join(all_dict) + "]")
		exit(1)
	if args.prim == args.sec:
		print("Given languages must be different. Given : \"{}\" and \"{}\"".format(args.prim, args.sec))
		exit(1)

	d = Dictcc()
	if len(args.word) > 0 and not args.console:
		d.handle_translation(args.word[0], args.prim, args.sec)
	else:
		d.handle_console(args.prim, args.sec)

if __name__ == '__main__':
	main()
