from tbollmeier.hwsim.builtin import Nand
from tbollmeier.hwsim.bit_value import BitValue
from tbollmeier.hwsim.composed_chip import ChipBuilder


Not = ChipBuilder()\
    .add_input("in")\
    .add_output("out")\
    .add_internal_part("nand", Nand)\
    .add_connection("in", "nand.a")\
    .set_input_bit("nand.b", BitValue.ONE)\
    .add_connection("nand.out", "out")

Or = ChipBuilder()\
    .add_input("a")\
    .add_input("b")\
    .add_output("out")\
    .add_internal_part("nota", Not)\
    .add_internal_part("notb", Not)\
    .add_internal_part("nand", Nand)\
    .add_connection("a", "nota.in")\
    .add_connection("nota.out", "nand.a")\
    .add_connection("b", "notb.in")\
    .add_connection("notb.out", "nand.b")\
    .add_connection("nand.out", "out")

And = ChipBuilder()\
    .add_input("a")\
    .add_input("b")\
    .add_output("out")\
    .add_internal_part("nand", Nand)\
    .add_internal_part("not", Not)\
    .add_connection("a", "nand.a")\
    .add_connection("b", "nand.b")\
    .add_connection("nand.out", "not.in")\
    .add_connection("not.out", "out")


if __name__ == "__main__":

    chip = And()

    for a in [0, 1]:
        chip.set_input_bit("a", a)
        for b in [0, 1]:
            chip.set_input_bit("b", b)
            out = chip.get_output("out").get_bits()[0]
            print(a, b, out)