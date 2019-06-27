from komparse import Parser, Grammar, Sequence, OneOf, \
    Optional, OneOrMore, Many


class _Grammar(Grammar):
    
    def __init__(self):
        Grammar.__init__(self, case_sensitive=True, wspace=[" ", "\t", "\r", "\n"])
        self._init_tokens()
        self._init_rules()
    
    def _init_tokens(self):
        self.add_comment('//', '\n')
        self.add_comment('/*', '*/')
        self.add_token('LBRACE', '{')
        self.add_token('RBRACE', '}')
        self.add_token('COMMA', ',')
        self.add_token('SEMICOLON', ';')
        self.add_token('ID', '[a-zA-Z][a-zA-Z0-9]*')
        self.add_keyword('CHIP')
        self.add_keyword('IN')
        self.add_keyword('OUT')
    
    def _init_rules(self):
        self.rule('chip', self._seq_1(), is_root=True)
        self.rule('inputs', self._seq_2())
        self.rule('input', self.ID())
        self.rule('outputs', self._seq_4())
        self.rule('output', self.ID())
    
    def _seq_1(self):
        return Sequence(
            self.CHIP(),
            self.ID('name'),
            self.LBRACE(),
            self.inputs(),
            self.outputs(),
            self.RBRACE())
    
    def _seq_2(self):
        return Sequence(
            self.IN(),
            self.input('in'),
            Many(self._seq_3()),
            self.SEMICOLON())
    
    def _seq_3(self):
        return Sequence(
            self.COMMA(),
            self.input('in'))
    
    def _seq_4(self):
        return Sequence(
            self.OUT(),
            self.output('out'),
            Many(self._seq_5()),
            self.SEMICOLON())
    
    def _seq_5(self):
        return Sequence(
            self.COMMA(),
            self.output('out'))
    
    
class HDLBaseParser(Parser):
    
    def __init__(self):
        Parser.__init__(self, _Grammar())
        
    
