from tbollmeier.hwsim.bit_value import BitValue


class Pins(object):

    def __init__(self, name, num_pins=1):
        self.name = name
        self.num_pins = num_pins

    def get_bits(self):
        return [BitValue.UNDEFINED for _ in range(self.num_pins)]


class Connector(Pins):

    def __init__(self, name, num_pins=1):
        Pins.__init__(self, name, num_pins)
        self._inbound_conns = []

    def connect(self, pins_source, pin_range_source=None, pin_range=None):
        range_src = pin_range_source is None and (0, pins_source.num_pins) or pin_range_source
        range_tgt = pin_range is None and (0, self.num_pins) or pin_range
        self._inbound_conns.append((range_tgt, pins_source, range_src))

    def get_bits(self):
        ret = [BitValue.UNDEFINED for _ in range(self.num_pins)]
        for my_range, pins_src, range_src in self._inbound_conns:
            pin_start, pin_end = my_range
            bits_src = pins_src.get_bits()
            pin_src, _ = range_src
            for pin in range(pin_start, pin_end):
                ret[pin] = bits_src[pin_src]
                pin_src += 1
        return ret


class Input(Connector):

    def __init__(self, name, num_pins=1):
        Connector.__init__(self, name, num_pins)
        self._bits = [BitValue.UNDEFINED for _ in range(self.num_pins)]

    def set_bit(self, value=BitValue.ONE, pin=0):
        self._bits[pin] = value

    def get_bits(self):
        if self._inbound_conns:
            ret = Connector.get_bits(self)
        else:
            ret = [BitValue.UNDEFINED for _ in range(self.num_pins)]
        for pin, value in enumerate(ret):
            if value == BitValue.UNDEFINED:
                ret[pin] = self._bits[pin]
        return ret


