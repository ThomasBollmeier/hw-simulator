import sys
import os.path
source_dir = os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "src"
sys.path.insert(0, source_dir)
from tbollmeier.hdl.hdl_parser import HDLParser


def test_parse():

    parser = HDLParser()

    hdl_code = """
    /** My first chip */
    CHIP MyChip {
    
    }
    """

    ast = parser.parse(hdl_code)
    print(ast.to_xml())


if __name__ == "__main__":

    test_parse()




