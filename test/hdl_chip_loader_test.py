import sys
import os.path
import unittest
source_dir = os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "src"
sys.path.insert(0, source_dir)
from tbollmeier.hdl.hdl_chip_loader import HDLChipLoader


class HDLParserTest(unittest.TestCase):

    def setUp(self):

        self._loader = HDLChipLoader()

    def test_load(self):

        builder = self._loader.get_chip_builder("Or")

        self.assertIsNotNone(builder)

        print(builder._connections)
        print(builder._input_bits)

        chip = builder()

        self.assertIsNotNone(chip)

        print(chip.get_input_names())
        print(chip.get_output_names())

        for a in [0, 1]:
            chip.set_input_bit('a', a)
            for b in [0, 1]:
                chip.set_input_bit('b', b)
                print(a, b, chip.get_output('out').get_bits()[0])


if __name__ == "__main__":

    unittest.main()




