import re


class BleHelper:
    @classmethod
    def uuid_filter(cls, uuid):
        return re.sub(r"[^0-9abcdef]", "", uuid.lower())
