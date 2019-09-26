import argparse as __argparse__

try:
	from dictcc import Dictcc as __Dictcc__
except ImportError:
	from dictcc.dictcc import Dictcc as __Dictcc__


def main():
	prim     = ['de', 'en']
	sec      = ['bg', 'bs', 'cs', 'da', 'el', 'eo', 'es', 'fi', 'fr', 'hr',
				'hu', 'is', 'it', 'la', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sk',
				'sq', 'sr', 'sv', 'tr']
	all_dict = prim + sec
	parser   = __argparse__.ArgumentParser(
			description='Query dict.cc for a translation.',
			formatter_class=__argparse__.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-p', '--prim', type=str, default='en', help='Primary language')
	parser.add_argument('-s', '--sec', type=str, default='de', help='Secondary language')
	parser.add_argument('-c', '--console', action='store_true')
	parser.add_argument('word', nargs=__argparse__.REMAINDER, help='word to translate')
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
	d = __Dictcc__()
	if len(args.word) > 0 and not args.console:
		d.handle_translation(args.word[0], args.prim, args.sec)
	else:
		d.handle_console(args.prim, args.sec)

if __name__ == '__main__':
	main()
