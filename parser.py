# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = { NAME, NUMBER, SKIP, IF, FI, DO, OD, BOOL, ASSIGN, COMP,
               LOGIC, NOT, ARROW, BR }
    ignore = ' \t'

    literals = { '+', '-', '*', '^', '/', '(', ')', ';'}    

    # Tokens
    SKIP            = r'skip'
    IF              = r'if '
    FI              = r'fi'
    DO              = r'do '
    OD              = r'od'
    BOOL            = r'true|false'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ASSIGN          = r':='
    COMP            = r'<=|>=|!=|=|<|>'
    LOGIC           = r'&&|\|\||&|\|'
    NOT             = r'!'
    ARROW           = r'->'
    BR              = r'\[\]'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        raise ValueError('ko')


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', UMINUS),
        )

    def __init__(self):
        self.names = { }

    @_('NAME ASSIGN expr')
    def C(self, p):
        self.names[p.NAME] = p.expr

    @_('SKIP')
    def C(self, p):
        pass

    @_('C ";" C')
    def C(self, p):
        pass

    @_('IF GC FI')
    def C(self, p):
        pass

    @_('DO GC OD')
    def C(self, p):
        pass

    @_('statement ARROW C')
    def GC(self, p):
        pass
    
    @_('GC BR GC')
    def GC(self, p):
        pass
        
    @_('statement LOGIC statement')
    def statement(self, p):
        pass

    @_('NOT statement')
    def statement(self, p):
        pass

    @_('expr COMP expr')
    def statement(self, p):
        pass

    @_('"(" statement ")"')
    def statement(self, p):
        pass

    @_('BOOL')
    def statement(self, p):
        pass   

    @_('expr "+" expr')
    def expr(self, p):
        pass

    @_('expr "-" expr')
    def expr(self, p):
        pass

    @_('expr "*" expr')
    def expr(self, p):
        pass

    @_('expr "/" expr')
    def expr(self, p):
        pass

    @_('expr "^" expr')
    def expr(self, p):
        pass

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        pass

    @_('"(" expr ")"')
    def expr(self, p):
        pass

    @_('NUMBER')
    def expr(self, p):
        pass

    @_('NAME')
    def expr(self, p):
        pass

    def error(self, t):
        raise ValueError('ko')

if __name__ == '__main__':
    expectedResults = ['ok', 'ok', 'ko', 'ok', 'ko', 'ok', 'ko', 'ok', 'ok', 'ko']
    lexer = CalcLexer()
    parser = CalcParser()

    for i in range(10):
        f = open("tests/test"+str(i)+".gcl", "r")
        print("-> Test"+str(i))
        try:
            parser.parse(lexer.tokenize(f.read()))
            result = 'ok'
        except:
            result = 'ko'
        print('Output:', result, 'Expected output:', expectedResults[i])
        if expectedResults[i] == result:
            print('Test'+str(i)+' passed!\n')
        else:
            print('Test'+str(i)+' failed!\n')
