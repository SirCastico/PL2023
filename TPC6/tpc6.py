import re
import ply.lex as lex

states = (
    ('blockcstate', 'exclusive'),
)

reserved = {
    'program' : 'PROGRAM',
    'function' : 'FUNCTION',
    'while' : 'WHILE',
    'for' : 'FOR',
    'in' : 'IN',
}

types = {
    'int' : 'INT'
}

tokens = (
    'NUM',
    'ID',

    'COMMENT',
    'BLOCKC_START',
    'BLOCKC_END',

    'SEMICOLON',
    'COLON',

    'INTERVAL',
    'EQUAL',
    'HIGHER',
    'LOWER',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',

    'L_CURV_BRCKT',
    'R_CURV_BRCKT',
    'L_CURLY_BRCKT',
    'R_CURLY_BRCKT',
    'L_SQUARE_BRCKT',
    'R_SQUARE_BRCKT',
) + tuple(reserved.values()) + tuple(types.values())


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'\w+'
    if t.value in reserved:
        t.type = reserved.get(t.value)
    elif t.value in types:
        t.type = types.get(t.value)
    return t

t_ignore_COMMENT = r'\/\/.*'

def t_ignore_BLOCKC_START(t):
    r'\/\*'
    t.lexer.begin('blockcstate')

#t_blockcstate_ignore_whynotwork = r"(^.+?(?=\*\/))|^.+$"
t_blockcstate_ignore_everything = r".+"
t_blockcstate_ignore = " \t\n"

def t_blockcstate_ignore_BLOCKC_END(t): 
    r'.*\*\/'
    t.lexer.begin('INITIAL')

t_SEMICOLON = r';'
t_COLON = r","
t_INTERVAL = r"\.\."

t_EQUAL = r'='
t_HIGHER = r'>'
t_LOWER = r'<'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'

t_L_CURV_BRCKT = r'\('
t_R_CURV_BRCKT = r'\)'
t_L_CURLY_BRCKT = r'{'
t_R_CURLY_BRCKT = r'}'
t_L_SQUARE_BRCKT = r'\['
t_R_SQUARE_BRCKT = r'\]'

t_ignore = " \t\n"

def t_ANY_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

data = """
/* factorial.p 
asd
*/ int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}
"""

lexer.input(data)

for tok in lexer:
    print(tok)
