from tbollmeier.hwsim.builtin import Nand
from tbollmeier.hwsim.bit_value import BitValue
from tbollmeier.hwsim.composed_chip import ComposedChip


def make_not():

    return ComposedChip()\
        .add_input("in")\
        .add_output("out")\
        .add_internal_part("nand", Nand())\
        .connect("in", "nand.a")\
        .set_input_bit("nand.b", BitValue.ONE)\
        .connect("nand.out", "out")


def make_or():

    chip = ComposedChip()
    chip.add_input("a").add_input("b").add_output("out")
    chip.add_internal_part("nota", make_not())
    chip.add_internal_part("notb", make_not())
    chip.add_internal_part("nand", Nand())
    chip.connect("a", "nota.in").connect("nota.out", "nand.a")
    chip.connect("b", "notb.in").connect("notb.out", "nand.b")
    chip.connect("nand.out", "out")

    return chip


if __name__ == "__main__":

    chip = make_or()

    for a in [0, 1]:
        chip.set_input_bit("a", a)
        for b in [0, 1]:
            chip.set_input_bit("b", b)
            out = chip.get_output("out").get_bits()[0]
            print(a, b, out)