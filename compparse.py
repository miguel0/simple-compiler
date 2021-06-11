import ply.yacc as yacc
from complex import tokens
from complex import lexer

class Node:
	def __init__(self, type, children=None):
		self.type = type
		if children:
			self.children = children
		else:
			self.children = []

def printChildren(node):
	if isinstance(node, Node):
		print(node.type)
		if node.children:
			for i in node.children:
				printChildren(i)
	else:
		print(node)

def p_block(p):
	'''block : stmt block
			 | stmt
			 | empty
	'''
	if len(p) == 3:
		p[0] = Node('block', [p[1], p[2]])
	elif p[1]:
		p[0] = p[1]

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
	p[0] = p[1]

def p_dcl(p):
	'''dcl : type ID ';'
		   | type ID '=' expr ';'
	'''
	if len(p) == 4:
		p[0] = Node('dcl', [p[1], p[2]])
	else:
		p[0] = Node('dclassign', [p[1], p[2], p[4]])

def p_type(p):
	'''type : BOOL
			| INT
			| FLOAT
			| STRING
	'''
	p[0] = p[1]

def p_expr(p):
	'''expr : boolexpr
			| numexpr
			| strexpr
	'''
	p[0] = p[1]

def p_boolexpr_bool(p):
	'''boolexpr : '(' boolexpr ')'
				| boolconst
				| ID
				| boolexpr boolop boolexpr
				| ID boolop boolexpr
	'''
	if p[1] == '(':
		p[0] = Node('bool', [p[2]])
	elif len(p) == 2:
		p[0] = Node('bool', [p[1]])
	else:
		p[0] = Node('boolop', [p[1], p[2], p[3]])

def p_boolexpr_num(p):
	'''boolexpr : numexpr comp numexpr
	'''
	p[0] = Node('numcomp', [p[1], p[2], p[3]])

def p_boolconst(p):
	'''boolconst : TRUE
				 | FALSE
	'''
	p[0] = p[1]

def p_comp(p):
	'''comp : LT
			| LE
			| GT
			| GE
			| EQ
			| NE
	'''
	p[0] = p[1]

def p_boolop(p):
	'''boolop : AND
			  | OR
	'''
	p[0] = p[1]

def p_numexpr(p):
	'''numexpr : '(' numexpr ')'
			   | ICONST
			   | FCONST
			   | ID
			   | numexpr numop numexpr
			   | ID numop numexpr 
	'''
	if p[1] == '(':
		p[0] = Node('num', p[2])
	if len(p) == 2:
		p[0] = Node('num', p[1])
	else:
		p[0] = Node('numop', [p[1], p[2], p[3]])

def p_numop(p):
	'''numop : '+'
			 | '-'
			 | '*'
			 | '/'
			 | '^'
	'''
	p[0] = p[1]

def p_strexpr(p):
	'''strexpr : SCONST
			   | STRING '(' numexpr ')'
			   | ID
			   | strexpr '+' strexpr
			   | ID '+' strexpr
	'''
	if len(p) == 4:
		p[0] = Node('concat', [p[1], p[3]])
	elif len(p) == 5:
		p[0] = Node('strcast', [p[3]])
	else:
		p[0] = Node('str', [p[1]])

def p_assign(p):
	'''assign : ID '=' expr ';'
	'''
	p[0] = Node('assign', [p[1], p[3]])

def p_cond(p):
	'''cond : IF '(' boolexpr ')' '{' block '}' elifs else
	'''
	p[0] = Node('if', [p[3], p[6]])
	if p[8]:
		p[0].children.append(p[8])
	if p[9]:
		p[0].children.append(p[9])

def p_elifs(p):
	'''elifs : ELIF '(' boolexpr ')' '{' block '}' elifs
			 | empty
	'''
	if len(p) > 2:
		p[0] = Node('elif', [p[3], p[6]])
		if p[8]:
			p[0].children.append(p[8])

def p_else(p):
	'''else : ELSE '{' block '}'
			| empty
	'''
	if len(p) > 2:
		p[0] = Node('else', [p[3]])

def p_loop(p):
	'''loop : for
			| while
			| dowhile
	'''
	p[0] = p[1]

def p_for(p):
	'''for : FOR '(' simpexpr ';' boolexpr ';' simpexpr ')' '{' block '}'
	'''
	p[0] = Node('for', [p[3], p[5], p[7], p[10]])

def p_simpexpr(p):
	'''simpexpr : type ID
				| type ID '=' expr
				| ID '=' expr
	'''
	if len(p) == 3:
		p[0] = Node('dcl', [p[1], p[2]])
	elif len(p) == 5:
		p[0] = Node('dclassign', [p[1], p[2], p[4]])
	else:
		p[0] = Node('assign', [p[1], p[3]])

def p_while(p):
	'''while : WHILE '(' boolexpr ')' '{' block '}'
	'''
	p[0] = Node('while', [p[3], p[6]])

def p_dowhile(p):
	'''dowhile : DO '{' block '}' WHILE '(' boolexpr ')' ';'
	'''
	p[0] = Node('dowhile', [p[3], p[7]])

parser = yacc.yacc()
res = parser.parse(lexer=lexer, input=open("input.txt").read())
# printChildren(res)

var = -1
label = -1
tac_str = ""
line = 0
label_stack = []

def write_line(*argv):
	global tac_str
	global line

	for arg in argv:
		tac_str += (arg + ' ')
	tac_str = tac_str[:-1]
	tac_str += '\n'
	line += 1

def get_var():
	global var
	var += 1
	return 'r' + str(var)

def get_label():
	global label
	label += 1
	return 'L' + str(label)

def add_line_num(my_str):
	arr = my_str.split('\n')
	for i in range(len(arr)):
		arr[i] = str(i) + '. ' + arr[i]
	return '\n'.join(arr)

def gen_tac(node):
	if not isinstance(node, Node):
		return node
	
	global line
	global label_stack
	c = node.children

	if node.type == 'block':
		gen_tac(c[0])
		if len(c) == 2:
			gen_tac(c[1])
	if node.type == 'dcl':
		pass
	if node.type == 'dclassign':
		write_line(c[1], '=', gen_tac(c[2]))
	if node.type == 'bool':
		return gen_tac(c[0])
	if node.type == 'boolop':
		v = get_var()
		write_line(v, '=', gen_tac(c[0]), c[1], gen_tac(c[2]))
		return v
	if node.type == 'numcomp':
		v = get_var()
		write_line(v, '=', gen_tac(c[0]), c[1], gen_tac(c[2]))
		return v
	if node.type == 'num':
		return gen_tac(c)
	if node.type == 'numop':
		v = get_var()
		write_line(v, '=', gen_tac(c[0]), c[1], gen_tac(c[2]))
		return v
	if node.type == 'concat':
		v = get_var()
		write_line(v, '=', gen_tac(c[0]), '+', gen_tac(c[1]))
		return v
	if node.type == 'strcast':
		v = get_var()
		write_line(v, '=', 'num2str(', gen_tac(c[0]), ')')
		return v
	if node.type == 'str':
		return gen_tac(c[0])
	if node.type == 'assign':
		write_line(c[0], '=', gen_tac(c[1]))
	if node.type == 'if':
		if len(c) == 4:
			label1 = get_label()
			label2 = get_label()
			label_stack.append(label2)

			write_line('if', 'false', gen_tac(c[0]), 'goto', label1)
			gen_tac(c[1])
			write_line('goto', label2)
			write_line(label1)
			gen_tac(c[2])
			gen_tac(c[3])
			write_line(label_stack.pop())			
		elif len(c) == 3:
			label1 = get_label()
			label2 = get_label()
			label_stack.append(label2)

			write_line('if', 'false', gen_tac(c[0]), 'goto', label1)
			gen_tac(c[1])
			write_line('goto', label2)
			write_line(label1)
			gen_tac(c[2])
			write_line(label_stack.pop())
		else:
			label = get_label()
			write_line('if', 'false', gen_tac(c[0]), 'goto', label)
			gen_tac(c[1])
			write_line(label)
	if node.type == 'elif':
		if len(c) == 3:
			label = get_label()
			write_line('if', 'false', gen_tac(c[0]), 'goto', label)
			gen_tac(c[1])
			write_line('goto', label_stack[-1])
			write_line(label)
			gen_tac(c[2])
		else:
			label = get_label()
			write_line('if', 'false', gen_tac(c[0]), 'goto', label)
			gen_tac(c[1])
			write_line('goto', label_stack[-1])
			write_line(label)
	if node.type == 'else':
		gen_tac(c[0])
	if node.type == 'for':
		label1 = get_label()
		label2 = get_label()

		gen_tac(c[0])
		write_line(label1)
		write_line('if', 'false', gen_tac(c[1]), 'goto', label2)
		gen_tac(c[3])
		gen_tac(c[2])
		write_line('goto', label1)
		write_line(label2)
	if node.type == 'while':
		label1 = get_label()
		label2 = get_label()

		write_line(label1)
		write_line('if', 'false', gen_tac(c[0]), 'goto', label2)
		gen_tac(c[1])
		write_line('goto', label1)
		write_line(label2)
	if node.type == 'dowhile':
		label1 = get_label()
		label2 = get_label()

		write_line(label1)
		gen_tac(c[0])
		write_line('if', 'false', gen_tac(c[1]), 'goto', label2)
		write_line('goto', label1)
		write_line(label2)

gen_tac(res)
tac_str = add_line_num(tac_str)
print(tac_str)
