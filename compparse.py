import ply.yacc as yacc
from complex import tokens
from complex import lexer

def p_block(p):
	'''block : stmt block
			 | stmt
			 | empty
	'''
	p[0] = 'buebos'

def p_empty(p):
	'''empty :
	'''
	pass

def p_stmt(p):
	'''stmt : dcl
			| assign
			| cond
			| loop
	'''
	pass

def p_dcl(p):
	'''dcl : type ID ';'
		   | type ID '=' expr ';'
	'''
	pass

def p_type(p):
	'''type : BOOL
			| INT
			| FLOAT
			| STRING
	'''
	pass

def p_expr(p):
	'''expr : boolexpr
			| numexpr
			| strexpr
	'''
	pass

def p_boolexpr(p):
	'''boolexpr : '(' boolexpr ')'
				| boolconst
				| ID
				| numexpr comp numexpr
				| boolexpr boolop boolexpr
	'''
	pass

def p_boolconst(p):
	'''boolconst : TRUE
				 | FALSE
	'''
	pass

def p_comp(p):
	'''comp : LT
			| LE
			| GT
			| GE
			| EQ
			| NE
	'''
	pass

def p_boolop(p):
	'''boolop : AND
			  | OR
	'''
	pass

def p_numexpr(p):
	'''numexpr : '(' numexpr ')'
			   | ICONST
			   | FCONST
			   | ID
			   | numexpr numop numexpr
	'''
	pass

def p_numop(p):
	'''numop : '+'
			 | '-'
			 | '*'
			 | '/'
			 | '^'
	'''
	pass

def p_strexpr(p):
	'''strexpr : SCONST
			   | STRING '(' numexpr ')'
			   | ID
			   | strexpr '+' strexpr
	'''
	pass

def p_assign(p):
	'''assign : ID '=' expr ';'
	'''
	pass

def p_cond(p):
	'''cond : IF '(' boolexpr ')' '{' block '}' elifs else
	'''
	pass

def p_elifs(p):
	'''elifs : ELIF '(' boolexpr ')' '{' block '}' elifs
			 | empty
	'''
	pass

def p_else(p):
	'''else : ELSE '{' block '}'
			| empty
	'''
	pass

def p_loop(p):
	'''loop : for
			| while
			| dowhile
	'''
	pass

def p_for(p):
	'''for : FOR '(' simpexpr ';' boolexpr ';' simpexpr ')' '{' block '}'
	'''
	pass

def p_simpexpr(p):
	'''simpexpr : type ID
				| type ID '=' expr
				| ID '=' expr
	'''
	pass

def p_while(p):
	'''while : WHILE '(' boolexpr ')' '{' block '}'
	'''
	pass

def p_dowhile(p):
	'''dowhile : DO '{' block '}' WHILE '(' boolexpr ')' ';'
	'''
	pass

parser = yacc.yacc()
print(parser.parse(lexer=lexer, input=open("input.txt").read()))
