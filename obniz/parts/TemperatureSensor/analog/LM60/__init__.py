from obniz.obniz.libs.utils.attr_default import AttrDefault
from .. import AnalogTemplatureSensor

class LM60(AnalogTemplatureSensor):
    @staticmethod
    def info():
        return AttrDefault(bool, {'name': 'LM60'})

    def calc(self, voltage):
        return round(((voltage - 0.424) / 0.00625) * 10) / 10.0