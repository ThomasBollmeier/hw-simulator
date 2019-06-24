from tbollmeier.hwsim.chip import Chip
from tbollmeier.hwsim.connector import Connector, Input


class ComponentType(object):

    INPUT = 1
    OUTPUT = 2
    INTERNAL = 3


class ChipBuilder(object):

    def __init__(self):
        self._inputs = []
        self._outputs = []
        self._parts = []
        self._connections = []
        self._input_bits = []

    def add_input(self, name, num_pins=1):
        self._inputs.append((name, num_pins))
        return self

    def add_output(self, name, num_pins=1):
        self._outputs.append((name, num_pins))
        return self

    def add_internal_part(self, name, chip_builder):
        self._parts.append((name, chip_builder))
        return self

    def add_connection(self, name_src, name_tgt, pin_range_src=None, pin_range_tgt=None):
        self._connections.append((name_src, name_tgt, pin_range_src, pin_range_tgt))
        return self

    def set_input_bit(self, full_name, value, pin=0):
        self._input_bits.append((full_name, value, pin))
        return self

    def __call__(self):
        chip = ComposedChip()
        for name, num_pins in self._inputs:
            chip.add_input(name, num_pins)
        for name, num_pins in self._outputs:
            chip.add_output(name, num_pins)
        for name, chip_builder in self._parts:
            chip.add_internal_part(name, chip_builder())
        for source, target, pin_range_src, pin_range_tgt in self._connections:
            chip.connect(source, target, pin_range_src, pin_range_tgt)
        for full_name, value, pin in self._input_bits:
            chip.set_input_bit(full_name, value, pin)
        return chip


class ComposedChip(Chip):

    def __init__(self):
        self._pins = {}

    def add_input(self, name, num_pins=1):
        self._pins[name] = (Input(name, num_pins), ComponentType.INPUT)
        return self

    def add_output(self, name, num_pins=1):
        self._pins[name] = (Connector(name, num_pins), ComponentType.OUTPUT)
        return self

    def add_internal_part(self, name, chip):
        input_names = chip.get_input_names()
        output_names = chip.get_output_names()
        for input_name in input_names:
            input_ = chip.get_input(input_name)
            self._pins[name + "." + input_name] = (input_, ComponentType.INTERNAL)
        for output_name in output_names:
            output = chip.get_output(output_name)
            self._pins[name + "." + output_name] = (output, ComponentType.INTERNAL)
        return self

    def connect(self, name_src, name_tgt, pin_range_src=None, pin_range_tgt=None):
        target, _ = self._pins[name_tgt]
        source, _ = self._pins[name_src]
        target.connect(source, pin_range_src, pin_range_tgt)
        return self

    def get_input_names(self):
        return [input_.name for input_, type_ in self._pins.values() if type_ == ComponentType.INPUT]

    def get_output_names(self):
        return [output_.name for output_, type_ in self._pins.values() if type_ == ComponentType.OUTPUT]

    def get_input(self, name):
        try:
            input_, type_ = self._pins[name]
            if type_ == ComponentType.INPUT:
                return input_
            else:
                return None
        except KeyError:
            return None

    def set_input_bit(self, full_name, value, pin=0):
        input_, _ = self._pins[full_name]
        input_.set_bit(value, pin)
        return self

    def get_output(self, name):
        try:
            output_, type_ = self._pins[name]
            if type_ == ComponentType.OUTPUT:
                return output_
            else:
                return None
        except KeyError:
            return None
