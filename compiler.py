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
)

literals = [
	'(', ')', '{', '}',
	'+', '-', '*', '/', '^',
	'==', '!=', '>', '<', '>=', '<=',
	'=', ';',
]
