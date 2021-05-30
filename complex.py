import ply.lex as lex

reserved = (
	'BOOL', 'INT', 'FLOAT', 'STRING',
	'IF', 'ELIF', 'ELSE',
	'FOR', 'DO', 'WHILE',
	'AND', 'OR',
	'TRUE', 'FALSE',
)

tokens = reserved + (
	'ID', 'ICONST', 'FCONST', 'SCONST',
	'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
)

literals = [
	'(', ')', '{', '}',
	'+', '-', '*', '/', '^',
	'=', ';',
]

t_ignore = ' \t'

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

reserved_map = {}
for r in reserved:
	reserved_map[r.lower()] = r

def t_ID(t):
	r'[A-Za-z_][\w_]*'
	t.type = reserved_map.get(t.value, "ID")
	return t

def t_error(t):
	print("Illegal character %s" % repr(t.value[0]))
	t.lexer.skip(1)

t_ICONST = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

t_FCONST = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

lexer = lex.lex()
if __name__ == "__main__":
	lex.runmain(lexer)
