import sys
import os.path
import unittest
source_dir = os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "src"
sys.path.insert(0, source_dir)
from tbollmeier.hdl.hdl_chip_factory import HDLChipFactory


class HDLParserTest(unittest.TestCase):

    def setUp(self):

        self._factory = HDLChipFactory()

    def test_load(self):

        chip_name = "Or2"

        builder = self._factory.get_chip_builder(chip_name)

        self.assertIsNotNone(builder)

        print(builder._connections)
        print(builder._input_bits)

        chip = self._factory.get_chip(chip_name)

        self.assertIsNotNone(chip)

        print(chip.get_input_names())
        print(chip.get_output_names())

        for a in [0, 1]:
            chip.set_input_bit('in', a, 0)
            for b in [0, 1]:
                chip.set_input_bit('in', b, 1)
                print(a, b, chip.get_output('out').get_bits()[0])


if __name__ == "__main__":

    unittest.main()




