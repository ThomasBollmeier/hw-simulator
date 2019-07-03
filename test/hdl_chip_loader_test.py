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

        chip = self._loader.get_chip("Not")

        self.assertIsNotNone(chip)

        print(chip.get_input_names())
        print(chip.get_output_names())


if __name__ == "__main__":

    unittest.main()




