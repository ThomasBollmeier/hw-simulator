import sys
import os.path
import unittest
source_dir = os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "src"
sys.path.insert(0, source_dir)
from tbollmeier.hdl.hdl_parser import HDLParser


class HDLParserTest(unittest.TestCase):

    def setUp(self):

        self._parser = HDLParser()

    def test_parse(self):

        hdl_code = """
/** My first chip */
 CHIP Not {

    IN in;
    OUT out;

    PARTS:
    Nand(a=in, b=true, out=out);

}
"""

        ast = self._parser.parse(hdl_code)
        self.assertIsNotNone(ast, self._parser.error())

        print(ast.to_xml())


if __name__ == "__main__":

    unittest.main()




