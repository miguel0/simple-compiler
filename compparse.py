import ply.yacc as yacc
from complex import tokens

def p_block(p):
	'''block : stmt block
			 | stmt'''
	pass

def p_stmt(p):
	'''stmt : dcl
			| assign
			| cond
			| loop'''
	pass

def p_dcl(p):
	'''dcl : type ID ';'
		   | type ID '=' expr ';''''
	pass

def p_type(p):
	'''type : BOOL
			| INT
			| FLOAT
			| STRING'''
	pass

def p_expr(p):
	'''expr : boolexpr
			| numexpr
			| strexpr'''
	pass

def p_boolexpr(p):
	'''boolexpr : '(' boolexpr ')'
				| boolconst
				| ID
				| numexpr comp numexpr
				| boolexpr boolop boolexpr'''
	pass

def p_boolconst(p):
	'''boolconst : TRUE
				 | FALSE'''
	pass

def p_comp(p):
	'''comp : LT
			| LE
			| GT
			| GE
			| EQ
			| NE'''
	pass

def p_boolop(p):
	'''boolop : AND
			  | OR'''
	pass

def p_numexpr(p):
	'''numexpr : '(' numexpr ')'
			   | ICONST
			   | FCONST
			   | ID
			   | numexpr numop numexpr'''
	pass

def p_numop(p):
	'''numop | '+'
			 | '-'
			 | '*'
			 | '/'
			 | '^''''
	pass

def p_strexpr(p):
	'''strexpr : SCONST
			  | ID
			  | strexpr '+' strexpr
			  | strexpr '+' numexpr'''
	pass

def p_assign(p):
	'''assign : ID '=' expr ';''''
	pass
