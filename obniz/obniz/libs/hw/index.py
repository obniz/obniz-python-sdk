import json
import os
import re


class HW:
    @staticmethod
    def get_definition_for(hw):
        if type(hw) is not str or not re.match(r"^[a-z0-9_]+$", hw):
            return None

        path = os.path.join(os.path.dirname(__file__), hw + '.json')
        if not os.path.isfile(path):
            return None

        with open(path) as f:
            return json.load(f)
