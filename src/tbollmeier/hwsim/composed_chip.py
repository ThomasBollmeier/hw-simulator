from tbollmeier.hwsim.chip import Chip
from tbollmeier.hwsim.connector import Connector, Input


class ComponentType(object):

    INPUT = 1
    OUTPUT = 2
    INTERNAL = 3


class ComposedChip(Chip):

    def __init__(self):
        self._parts = {}

    def add_input(self, name, num_pins=1):
        self._parts[name] = (Input(name, num_pins), ComponentType.INPUT)
        return self

    def add_output(self, name, num_pins=1):
        self._parts[name] = (Connector(name, num_pins), ComponentType.OUTPUT)
        return self

    def add_internal_part(self, name, chip):
        input_names = chip.get_input_names()
        output_names = chip.get_output_names()
        for input_name in input_names:
            input_ = chip.get_input(input_name)
            self._parts[name + "." + input_name] = (input_, ComponentType.INTERNAL)
        for output_name in output_names:
            output = chip.get_output(output_name)
            self._parts[name + "." + output_name] = (output, ComponentType.INTERNAL)
        return self

    def connect(self, name_src, name_tgt, pin_range_src=None, pin_range_tgt=None):
        target, _ = self._parts[name_tgt]
        source, _ = self._parts[name_src]
        target.connect(source, pin_range_src, pin_range_tgt)
        return self

    def get_input_names(self):
        return [input_.name for input_, type_ in self._parts.values() if type_ == ComponentType.INPUT]

    def get_output_names(self):
        return [output_.name for output_, type_ in self._parts.values() if type_ == ComponentType.OUTPUT]

    def get_input(self, name):
        try:
            input_, type_ = self._parts[name]
            if type_ == ComponentType.INPUT:
                return input_
            else:
                return None
        except KeyError:
            return None

    def set_input_bit(self, full_name, value, pin=0):
        input_, _ = self._parts[full_name]
        input_.set_bit(value, pin)
        return self

    def get_output(self, name):
        try:
            output_, type_ = self._parts[name]
            if type_ == ComponentType.OUTPUT:
                return output_
            else:
                return None
        except KeyError:
            return None
