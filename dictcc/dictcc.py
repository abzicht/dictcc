#!/usr/bin/python3

import sys
import requests
import argparse
import os
import textwrap

from tabulate import tabulate
from bs4 import BeautifulSoup

class Dictcc:

	def __init__(self, prim, sec, word=None):
		_, self.columns          = os.popen('stty size', 'r').read().split()
		self.requests_session    = requests.Session()
		self.primary_lang        = prim
		self.secondary_lang      = sec
		self.word                = word
		self.current_suggestions = []
		self.console             = self.word is None


	def run(self):
		if self.console:
			self.handle_console()
		else:
			self.handle_translation(self.word)

	def request(self, word, f, t):
		header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
		payload = {'s': word}
		r = self.requests_session.get(
				"https://{}{}.dict.cc/".format(f, t),
				headers=header,
				params=payload)
		return r.content

	def parse_single_tag(self, tag):
		str_tag = " ".join([a_tag.text for a_tag in tag.find_all('a')])
		if (tag.dfn):
			all_dfn = ", ".join([dfn_tag.text for dfn_tag in tag.find_all('dfn')])
			str_tag = ' '.join([str_tag, '(' + all_dfn + ')'])
		return '\n   '.join(textwrap.wrap(str_tag, (int(self.columns) - 8) / 2))

	def parse_response(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		data = [tag for tag in soup.find_all('td', 'td7nl')]
		raw_from_to = zip(data[::2], data[1::2])
		res_from_to = list()
		for f, t in raw_from_to:
			res_from_to.append([self.parse_single_tag(f), self.parse_single_tag(t)])
		return res_from_to

	def parse_suggestions(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		data = [tag.a.text for tag in soup.find_all('td', 'td3nl') if tag.a]
		return data

	def handle_translation(self, word):
		try:
			word = self.current_suggestions[int(word) - 1]
		except (ValueError, IndexError) as e:
			# act like nothing happened. seems like 'word' really was
			# meant to be a word
			pass
		c = None
		try:
			c = self.request(word, self.primary_lang, self.secondary_lang)
		except Exception as e:
			print("While querying dict.cc, the following error occurred")
			print(e)
			return
		data = self.parse_response(c)
		if data:
			print(tabulate(data, [self.primary_lang, self.secondary_lang], tablefmt='orgtbl'))
			self.current_suggestions = []
		else:
			print(' '.join(["No translation found for:", word]))
			suggestions = self.parse_suggestions(c)
			self.current_suggestions = suggestions

			print('\nSuggestions given by dict.cc'
					+ 'choose by entering the number)' if self.console else ''
					+ ':')
			for i,s in enumerate(suggestions):
				if self.console:
					print(" - {}: {}".format(i+1, s))
				else:
					print(" - {}".format(s))

	def handle_console(self):
		print('Enter a word for translation')
		print('Enter q or hit CTRL+C for exit')
		try:
			user_input = None
			while user_input != 'q':
				user_input = input('> ')
				self.handle_translation(user_input)
		except KeyboardInterrupt:
			return

def main():
	prim = ['de', 'en']
	sec = ['bg', 'bs', 'cs', 'da', 'el', 'eo', 'es', 'fi', 'fr', 'hr',
			'hu', 'is', 'it', 'la', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sk',
			'sq', 'sr', 'sv', 'tr']
	all_dict = prim + sec
	parser = argparse.ArgumentParser(
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

	d = Dictcc(args.prim, args.sec, args.word[0] if len(args.word) > 0 and not args.console else None)
	d.run()

if __name__ == '__main__':
	main()
