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
        self.add_token('LBRACKET', '\[')
        self.add_token('RBRACKET', '\]')
        self.add_token('LPAR', '\(')
        self.add_token('RPAR', '\)')
        self.add_token('DOT2', '\.\.')
        self.add_token('COMMA', ',')
        self.add_token('SEMICOLON', ';')
        self.add_token('COLON', ':')
        self.add_token('EQ', '=')
        self.add_token('TRUE', 'true')
        self.add_token('FALSE', 'false')
        self.add_token('ID', '[a-zA-Z][a-zA-Z0-9]*')
        self.add_token('POS_INT', '[1-9][0-9]*')
        self.add_token('INT', '0|[1-9][0-9]*')
        self.add_token('PARTS', 'PARTS')
        self.add_keyword('CHIP')
        self.add_keyword('IN')
        self.add_keyword('OUT')
    
    def _init_rules(self):
        self.rule('chip', self._seq_1(), is_root=True)
        self.rule('inputs', self._seq_2())
        self.rule('inout', self._seq_4())
        self.rule('outputs', self._seq_6())
        self.rule('parts', self._seq_8())
        self.rule('part', self._seq_9())
        self.rule('connection', self._seq_11())
        self.rule('value', self._oneof_2())
    
    def _seq_1(self):
        return Sequence(
            self.CHIP(),
            self.ID('name'),
            self.LBRACE(),
            OneOrMore(self._oneof_1()),
            self.parts(),
            self.RBRACE())
    
    def _seq_10(self):
        return Sequence(
            self.COMMA(),
            self.connection('conn'))
    
    def _seq_11(self):
        return Sequence(
            self.ID('param'),
            Optional(self._seq_12()),
            self.EQ(),
            self.value())
    
    def _seq_12(self):
        return Sequence(
            self.LBRACKET(),
            self.INT('from'),
            self.DOT2(),
            self.INT('to'),
            self.RBRACKET())
    
    def _seq_13(self):
        return Sequence(
            self.ID('pin'),
            Optional(self._seq_14()))
    
    def _seq_14(self):
        return Sequence(
            self.LBRACKET(),
            self.INT('from'),
            self.DOT2(),
            self.INT('to'),
            self.RBRACKET())
    
    def _seq_2(self):
        return Sequence(
            self.IN(),
            self.inout('in'),
            Many(self._seq_3()),
            self.SEMICOLON())
    
    def _seq_3(self):
        return Sequence(
            self.COMMA(),
            self.inout('in'))
    
    def _seq_4(self):
        return Sequence(
            self.ID(),
            Optional(self._seq_5()))
    
    def _seq_5(self):
        return Sequence(
            self.LBRACKET(),
            self.POS_INT('size'),
            self.RBRACKET())
    
    def _seq_6(self):
        return Sequence(
            self.OUT(),
            self.inout('out'),
            Many(self._seq_7()),
            self.SEMICOLON())
    
    def _seq_7(self):
        return Sequence(
            self.COMMA(),
            self.inout('out'))
    
    def _seq_8(self):
        return Sequence(
            self.PARTS(),
            self.COLON(),
            OneOrMore(self.part('part')))
    
    def _seq_9(self):
        return Sequence(
            self.ID('chip'),
            self.LPAR(),
            self.connection('conn'),
            Many(self._seq_10()),
            self.RPAR(),
            self.SEMICOLON())
    
    def _oneof_1(self):
        return OneOf(
            self.inputs(),
            self.outputs())
    
    def _oneof_2(self):
        return OneOf(
            self.TRUE(),
            self.FALSE(),
            self._seq_13())
    
    
class HDLBaseParser(Parser):
    
    def __init__(self):
        Parser.__init__(self, _Grammar())
        
    
