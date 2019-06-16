# dict.cc commandline tool

This tool enables the use of [dict.cc](https://dict.cc) over the commandline.

```bash
python3 dictcc.py <word>
```

Install `dictcc` on your system via `python3 setup.py install`.

Enter the interactive cli mode via `-c`:

```bash
python3 dictcc.py -c
```

Available languages: de (prim), en (prim), bg, bs, cs, da, el, eo, es, fi, fr,
hr, hu, is, it, la, nl, no, pl, pt, ro, ru, sk, sq, sr, sv, tr.

Choose between languages with the flags `-p` (primary language)
and `-s` (secondary language).

## Module
Import the `dictcc` module into your project:
```python
>>> from dictcc.dictcc import Dictcc
>>> d = Dictcc()
>>> result, suggestions = d.translate('tree', 'en', 'de')
>>> print("Results:", result)
Results: [['tree [attr.]', 'Baum-'], ... ]

>>> result, suggestions = d.translate('dreiekig', 'en', 'de')
>>> print("Suggestions:", suggestions)
Suggestions: ['dreieckig']

```

## Requirements
Requires [tabulate](https://bitbucket.org/astanin/python-tabulate) and
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).

Run
```bash
pip install tabulate bs4
```
or execute the setup script.
