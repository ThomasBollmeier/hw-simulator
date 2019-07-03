from tbollmeier.hdl.hdl_parser import HDLParser
from tbollmeier.hwsim.builtin import Nand
from tbollmeier.hwsim.composed_chip import ChipBuilder


class HDLChipLoader(object):

    def __init__(self):
        self._parser = HDLParser()
        self._loaded = {}
        self._builtin = set("Nand")

    def get_chip(self, name):

        if name in self._builtin:
            return {
                "Nand": Nand()
            }[name]

        if name not in self._loaded:
            self._loaded[name] = self._load_chip_builder(name)

        return self._loaded[name]()

    def _load_chip_builder(self, name):

        hdl_code = self._get_hdl_code(name)

        chip_ast = self._parser.parse(hdl_code)
        if chip_ast is None:
            raise Exception(self._parser.error())

        return self._make_chip_builder(chip_ast)

    @staticmethod
    def _get_hdl_code(name):

        file_path = name + ".hdl"
        fp = open(file_path, "r")
        lines = fp.readlines()
        fp.close()

        code = ""
        for line in lines:
            code += line

        return code

    def _make_chip_builder(self, chip_ast):

        builder = ChipBuilder()

        for name, size in self._get_pins(chip_ast, "inputs"):
            builder.add_input(name, size)

        for name, size in self._get_pins(chip_ast, "outputs"):
            builder.add_output(name, size)

        return builder

    @staticmethod
    def _get_pins(chip_ast, category):

        ret = []
        pins_list = chip_ast.find_children_by_name(category)
        for pin_list in pins_list:
            pins = pin_list.get_children()
            for pin in pins:
                name = pin.get_attr("name")
                if pin.has_attr("bus-size"):
                    size = int(pin.get_attr("bus-size"))
                else:
                    size = 1
                ret.append((name, size))

        return ret



