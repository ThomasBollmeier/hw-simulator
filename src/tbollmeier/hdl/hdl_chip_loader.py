from tbollmeier.hdl.hdl_parser import HDLParser
from tbollmeier.hwsim.builtin import Nand
from tbollmeier.hwsim.composed_chip import ChipBuilder
from tbollmeier.hwsim.bit_value import BitValue


class HDLChipLoader(object):

    def __init__(self):
        self._parser = HDLParser()
        self._loaded = {}
        self._builtin = set(["Nand"])
        self._num_parts = 0
        self._connections = []
        self._input_bits = []

    def get_chip(self, name):

        return self._get_chip_builder(name)()

    def get_chip_builder(self, name):

        if name not in self._loaded:
            self._loaded[name] = self._load_chip_builder(name)

        return self._loaded[name]

    def _load_chip_builder(self, name):

        if name in self._builtin:
            return {
                "Nand": Nand
            }[name]

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
        inputs = {}
        outputs = {}

        for name, size in self._get_pins(chip_ast, "inputs"):
            builder.add_input(name, size)
            inputs[name] = size

        for name, size in self._get_pins(chip_ast, "outputs"):
            builder.add_output(name, size)
            outputs[name] = size

        parts = chip_ast.find_children_by_name("parts")

        if parts:

            parts_ast = parts[0]

            for part_ast in parts_ast.get_children():
                part_name = part_ast.get_attr('chip-name')
                part_builder = HDLChipLoader().get_chip_builder(part_name)
                part_id = "part_{}".format(self._num_parts)
                self._num_parts += 1
                builder.add_internal_part(part_id, part_builder)
                self._update_connections_and_input(part_id,
                                                   part_builder,
                                                   part_ast,
                                                   inputs,
                                                   outputs)

            for connection in self._connections:
                builder.add_connection(connection.source, connection.target)

            for full_name, value, bit in self._input_bits:
                builder.set_input_bit(full_name, value, bit)

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

    def _update_connections_and_input(self,
                                      part_id,
                                      part_builder,
                                      part_ast,
                                      inputs,
                                      outputs):

        part_chip = part_builder()
        part_input_names = part_chip.get_input_names()
        part_output_names = part_chip.get_output_names()

        for connection_ast in part_ast.get_children():

            connection_data = _ConnectionData()

            children = connection_ast.get_children()

            param_name = children[0].get_attr('name')
            if param_name in part_input_names:
                connection_data.target = part_id + "." + param_name
            elif param_name in part_output_names:
                connection_data.source = part_id + "." + param_name
            else:
                raise Exception("Unknown pin {}".format(param_name))

            arg = children[1]

            if arg.name == "true":
                if connection_data.target:
                    self._input_bits.append((connection_data.target, BitValue.ONE, 0))
            elif arg.name == "false":
                if connection_data.target:
                    self._input_bits.append((connection_data.target, BitValue.ZERO, 0))
            else:
                arg_name = arg.get_attr('name')
                if arg_name in inputs:
                    connection_data.source = arg_name
                    self._connections.append(connection_data)
                elif arg_name in outputs:
                    connection_data.target = arg_name
                    self._connections.append(connection_data)
                else:
                    connection_data.name = arg_name
                    found = False
                    for conn_data in self._connections:
                        if conn_data.name == arg_name:
                            found = True
                            if not conn_data.source:
                                conn_data.source = connection_data.source
                            if not conn_data.target:
                                conn_data.target = connection_data.target
                            break
                    if not found:
                        self._connections.append(connection_data)


class _ConnectionData(object):

    def __init__(self):
        self.source = ""
        self.target = ""
        self.name = ""