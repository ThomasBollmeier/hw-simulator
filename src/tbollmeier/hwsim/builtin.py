from tbollmeier.hwsim.bit_value import BitValue
from tbollmeier.hwsim.chip import Chip
from tbollmeier.hwsim.connector import Pins, Input


class Nand(Chip):

    def __init__(self):

        self._a = Input("a")
        self._b = Input("b")
        self._out = _NandOut(self)

    def get_input_names(self):
        return ["a", "b"]

    def get_output_names(self):
        return ["out"]

    def get_input(self, name):
        try:
            return {
                "a": self._a,
                "b": self._b
            }[name]
        except KeyError:
            return None

    def get_output(self, name):
        return name == "out" and self._out or None


class _NandOut(Pins):

    def __init__(self, nand):
        Pins.__init__(self, "out")
        self._nand = nand

    def get_bits(self):
        a = self._nand._a.get_bits()[0]
        b = self._nand._b.get_bits()[0]
        if a == BitValue.UNDEFINED or b == BitValue.UNDEFINED:
            return [BitValue.UNDEFINED]
        if a == BitValue.ONE and b == BitValue.ONE:
            return [BitValue.ZERO]
        else:
            return [BitValue.ONE]

