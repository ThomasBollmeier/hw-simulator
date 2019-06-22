from tbollmeier.hwsim.chip import Chip
from tbollmeier.hwsim.connector import Input, Connector
from tbollmeier.hwsim.builtin import Nand
from tbollmeier.hwsim.bit_value import BitValue


class Not(Chip):

    def __init__(self):

        self._in = Input("in")
        self._out = Connector("out")

        nand = Nand()
        nand.get_input("a").connect(self._in)
        nand.get_input("b").set_bit(BitValue.ONE)
        self._out.connect(nand.get_output("out"))

    def get_input_names(self):
        return ["in"]

    def get_output_names(self):
        return ["out"]

    def get_input(self, name):
        return name == "in" and self._in or None

    def get_output(self, name):
        return name == "out" and self._out or None


if __name__ == "__main__":

    chip = Not()

    for inval in [0,1]:
        chip.set_input_bit("in", inval)
        outval = chip.get_output("out").get_bits()[0]
        print(inval, outval)