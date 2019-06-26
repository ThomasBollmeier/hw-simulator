from tbollmeier.hdl.hdl_base_parser import HDLBaseParser
from komparse.ast import Ast


class HDLParser(HDLBaseParser):

    def __init__(self):

        HDLBaseParser.__init__(self)
        self._set_ast_transformations()

    def _set_ast_transformations(self):

        g = self._grammar
        g.set_ast_transform("chip", self._trans_chip)

    def _trans_chip(self, ast):

        ret = Ast("chip")
        ret.set_attr("name", ast.find_children_by_id('name')[0].value)

        return ret