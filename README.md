# dict.cc commandline tool

This tool enables the use of [dict.cc](https://dict.cc) over the command line.

## Install
Install `dictcc` on your system via
```bash
python3 setup.py install
```

## Usage
When installed, the tool can be used:
```bash
dictcc <word>
```
Enter an interactive cli mode by passing no argument or the `-c` flag:
```bash
dictcc -c
```

## Languages
Available languages: de (prim), en (prim), bg, bs, cs, da, el, eo, es, fi, fr,
hr, hu, is, it, la, nl, no, pl, pt, ro, ru, sk, sq, sr, sv, tr.

Choose between languages with the flags `-p` (primary language)
and `-s` (secondary language).

## Module
Import the `dictcc` module into your project:
```python
>>> import dictcc
>>> result1, suggestions1 = dictcc.translate('tree', 'en', 'de')
>>> print("Results:", result1)
Results: [['tree [attr.]', 'Baum-'], ... ]

>>> result2, suggestions2 = dictcc.translate('dreiekig', 'en', 'de')
>>> print("Suggestions:", suggestions2)
Suggestions: ['dreieckig']

```

## Requirements
This tool requires [tabulate](https://bitbucket.org/astanin/python-tabulate) and
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).
Both dependencies are installed automatically when running `python3 setup.py install`.

Alternatively, run:
```bash
pip install tabulate bs4
```
