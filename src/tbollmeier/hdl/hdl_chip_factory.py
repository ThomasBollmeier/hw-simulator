from tbollmeier.hdl.hdl_chip_loader import HDLChipLoader


class HDLChipFactory(object):

    def __init__(self):

        self._loaded = {}

    def get_chip_builder(self, chip_name):

        if chip_name not in self._loaded:
            self._loaded[chip_name] = HDLChipLoader(self).load_chip_builder(chip_name)

        return self._loaded[chip_name]

    def get_chip(self, chip_name):

        return self.get_chip_builder(chip_name)()
