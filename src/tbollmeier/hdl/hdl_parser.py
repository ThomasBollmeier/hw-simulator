from tbollmeier.hdl.hdl_base_parser import HDLBaseParser
from komparse.ast import Ast


class HDLParser(HDLBaseParser):

    def __init__(self):

        HDLBaseParser.__init__(self)
        self._set_ast_transformations()

    def _set_ast_transformations(self):

        g = self._grammar
        g.set_ast_transform("chip", self._trans_chip)
        g.set_ast_transform("inputs", self._trans_inputs)
        g.set_ast_transform("outputs", self._trans_outputs)
        g.set_ast_transform("input", self._trans_inout)
        g.set_ast_transform("output", self._trans_inout)

    def _trans_chip(self, ast):

        ret = Ast("chip")
        ret.set_attr("name", ast.find_children_by_id('name')[0].value)

        ret.add_children_by_name(ast, "inputs")
        ret.add_children_by_name(ast, "outputs")

        return ret

    def _trans_inputs(self, ast):

        ret = Ast("inputs")
        ret.add_children_by_id(ast, "in")

        return ret

    def _trans_outputs(self, ast):

        ret = Ast("outputs")
        ret.add_children_by_id(ast, "out")

        return ret

    def _trans_inout(self, ast):
        return ast.get_children()[0]
