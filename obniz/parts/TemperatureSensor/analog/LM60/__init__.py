from .. import AnalogTemplatureSensor
from attrdict import AttrDefault

class LM60(AnalogTemplatureSensor):
    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'LM60'})

    def calc(self, voltage):
        return round(((voltage - 0.424) / 0.00625) * 10) / 10.0