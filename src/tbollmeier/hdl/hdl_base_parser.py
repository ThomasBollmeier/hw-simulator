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
        self.add_token('ID', '[a-zA-Z][a-zA-Z0-9]*')
        self.add_keyword('CHIP')
    
    def _init_rules(self):
        self.rule('chip', self._seq_1(), is_root=True)
    
    def _seq_1(self):
        return Sequence(
            self.CHIP(),
            self.ID('name'),
            self.LBRACE(),
            self.RBRACE())
    
    
class HDLBaseParser(Parser):
    
    def __init__(self):
        Parser.__init__(self, _Grammar())

