class Chip(object):

    def get_input_names(self):
        return []

    def get_output_names(self):
        return []

    def get_input(self, name):
        return None

    def set_input_bit(self, name, value, pin=0):
        self.get_input(name).set_bit(value, pin)

    def get_output(self, name):
        return None
