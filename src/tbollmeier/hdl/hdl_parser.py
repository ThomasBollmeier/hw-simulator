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
        g.set_ast_transform("inout", self._trans_inout)
        g.set_ast_transform("parts", self._trans_parts)
        g.set_ast_transform("part", self._trans_part)
        g.set_ast_transform("connection", self._trans_connection)
        g.set_ast_transform("value", self._trans_value)

    def _trans_chip(self, ast):

        ret = Ast("chip")
        ret.set_attr("name", ast.find_children_by_id('name')[0].value)

        ret.add_children_by_name(ast, "inputs")
        ret.add_children_by_name(ast, "outputs")
        ret.add_children_by_name(ast, "parts")

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
        ret = Ast("pin")
        name = ast.get_children()[0]
        ret.set_attr("name", name.value)
        size = ast.find_children_by_id('size')
        if size:
            size = size[0]
            ret.set_attr("bus-size", size.value)
        return ret

    def _trans_parts(self, ast):
        ret = Ast('parts')
        ret.add_children_by_id(ast, "part")
        return ret

    def _trans_part(self, ast):
        ret = Ast('part')
        chip = ast.find_children_by_id("chip")[0].value
        ret.set_attr("chip-name", chip)
        ret.add_children_by_id(ast, "conn")
        return ret

    def _trans_connection(self, ast):
        ret = Ast('connection')
        lhs = Ast('pin')
        ret.add_child(lhs)
        lhs.set_attr("name", ast.find_children_by_id('param')[0].value)
        from_ = ast.find_children_by_id('from')
        if from_:
            from_ = from_[0].value
            to = ast.find_children_by_id('to')[0].value
            lhs.set_attr("from", from_)
            lhs.set_attr("to", to)
        value = ast.get_children()[-1]
        ret.add_child(value)
        return ret

    def _trans_value(self, ast):
        children = ast.get_children()
        if len(children) == 1:
            child = children[0]
            if child.name == "TRUE" or child.name == "FALSE":
                return Ast(child.name.lower())
        ret = Ast("pin")
        ret.set_attr("name", ast.find_children_by_id('pin')[0].value)
        from_ = ast.find_children_by_id('from')
        if from_:
            from_ = from_[0].value
            to = ast.find_children_by_id('to')[0].value
            ret.set_attr("from", from_)
            ret.set_attr("to", to)
        return ret
