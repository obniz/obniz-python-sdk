import os
import json

class HW:
    @staticmethod
    def get_definition_for(hw):
        if hw == 'obnizb1':
            with open(os.path.join(os.path.dirname(__file__), 'obnizb1.json')) as f:
                hw_obj = json.load(f)
        elif hw == 'obnizb2':
            with open(os.path.join(os.path.dirname(__file__), 'obnizb2.json')) as f:
                hw_obj = json.load(f)
        elif hw == 'esp32w':
            with open(os.path.join(os.path.dirname(__file__), 'esp32w.json')) as f:
                hw_obj = json.load(f)
        else:
            hw_obj = None
        return hw_obj
