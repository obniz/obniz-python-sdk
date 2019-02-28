class Display:
    def __init__(self, obniz):
        self.obniz = obniz
        self.width = 128
        self.height = 64

    # def font:

    def clear(self):
        obj = {}
        obj['display'] = {
            "clear": True
        }
        self.obniz.send(obj)

    # def pos:

    def print(self, text):
        obj = {}
        obj['display'] = {
            "text": text
        }
        self.obniz.send(obj)

    # def line
    # def rect
    # def circle
    
    def qr(self, text, correction="M"):
        obj = {}
        obj['display'] = {
            "qr": {
                "text": text,
                "correction": correction
            }
        }
        self.obniz.send(obj)
    
    def raw(self, data):
        obj = {}
        obj['display'] = {
            "raw": data
        }
        self.obniz.send(obj)

    def set_pin_name(self, io, module_name, func_name):
        obj = {}
        obj['display'] = {
            'pin_assign': {
                io: {
                    "module_name": module_name,
                    "pin_name": func_name
                }
            }
        }
        self.obniz.send(obj)

    def set_pin_names(self, module_name, data):
        obj = {}
        obj['display'] = {
            'pin_assign': {}
        }
        for key in data:
            obj['display']['pin_assign'][key] = {
                "module_name": module_name,
                "pin_name": data[key]
            }
        if data:
            self.obniz.send(obj)