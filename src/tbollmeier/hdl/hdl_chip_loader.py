from tbollmeier.hdl.hdl_parser import HDLParser
from tbollmeier.hwsim.builtin import Nand
from tbollmeier.hwsim.composed_chip import ChipBuilder
from tbollmeier.hwsim.bit_value import BitValue


class HDLChipLoader(object):

    def __init__(self, chip_factory):
        self._chip_factory = chip_factory
        self._parser = HDLParser()
        self._builtin = set(["Nand"])
        self._num_parts = 0
        self._connections = []
        self._input_bits = []

    def load_chip_builder(self, name):

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
                part_builder = self._chip_factory.get_chip_builder(part_name)
                part_id = "part_{}".format(self._num_parts)
                self._num_parts += 1
                builder.add_internal_part(part_id, part_builder)
                self._update_connections_and_input(part_id,
                                                   part_builder,
                                                   part_ast,
                                                   inputs,
                                                   outputs)

            for connection in self._connections:
                builder.add_connection(connection.source,
                                       connection.target,
                                       connection.pin_range_source,
                                       connection.pin_range_target)

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

            param = children[0]
            param_name = param.get_attr('name')

            # Pin range:
            if param.has_attr("from"):
                from_ = int(param.get_attr("from"))
                to = int(param.get_attr("to"))
                param_pin_range = (from_, to + 1)
            else:
                if param_name in part_input_names:
                    num_pins = part_chip.get_input(param_name).num_pins
                else:
                    num_pins = part_chip.get_output(param_name).num_pins
                param_pin_range = (0, num_pins)

            if param_name in part_input_names:
                connection_data.target = part_id + "." + param_name
                connection_data.pin_range_target = param_pin_range
            elif param_name in part_output_names:
                connection_data.source = part_id + "." + param_name
                connection_data.pin_range_source = param_pin_range
            else:
                raise Exception("Unknown pin {}".format(param_name))

            arg = children[1]

            if arg.name == "true" or arg.name == "false":
                if connection_data.target:
                    value = arg.name == "true" and BitValue.ONE or BitValue.ZERO
                    start, end = connection_data.pin_range_target
                    for pin in range(start, end):
                        self._input_bits.append((connection_data.target, value, pin))
            else:
                arg_name = arg.get_attr('name')

                if arg.has_attr('from'):
                    from_ = int(arg.get_attr('from'))
                    to = int(arg.get_attr("to"))
                    arg_pin_range = (from_, to + 1)
                else:
                    arg_pin_range = None

                if arg_name in inputs:
                    connection_data.source = arg_name
                    connection_data.pin_range_source = arg_pin_range
                    self._connections.append(connection_data)
                elif arg_name in outputs:
                    connection_data.target = arg_name
                    connection_data.pin_range_target = arg_pin_range
                    self._connections.append(connection_data)
                else:
                    connection_data.name = arg_name
                    found = False
                    for conn_data in self._connections:
                        if conn_data.name == arg_name:
                            found = True
                            if not conn_data.source:
                                conn_data.source = connection_data.source
                                from_, to = conn_data.pin_range_target
                                conn_data.pin_range_source = (0, to - from_)
                            if not conn_data.target:
                                conn_data.target = connection_data.target
                                from_, to = conn_data.pin_range_source
                                conn_data.pin_range_source = (0, to - from_)
                            break
                    if not found:
                        self._connections.append(connection_data)


class _ConnectionData(object):

    def __init__(self):
        self.source = ""
        self.pin_range_source = None
        self.target = ""
        self.pin_range_target = None
        self.name = ""
