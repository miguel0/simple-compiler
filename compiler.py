import ply.lex as lex

reserved = (
	'BOOL', 'INT', 'FLOAT', 'STRING',
	'IF', 'ELIF', 'ELSE',
	'FOR', 'DO', 'WHILE',
	'AND', 'OR',
)

tokens = reserved + (
	'ID', 'BCONST', 'ICONST', 'FCONST', 'SCONST',
)

literals = [
	'(', ')', '{', '}',
	'+', '-', '*', '/', '^',
	'==', '!=', '>', '<', '>=', '<=',
	'=', ';',
]
