from dictcc.dictcc import Dictcc as __Dictcc__

__d__ = None
def translate(word, prim, sec):
	global __d__
	if __d__ is None:
		__d__ = __Dictcc__()
	return __d__.translate(word, prim, sec)
