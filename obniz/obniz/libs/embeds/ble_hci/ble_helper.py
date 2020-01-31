import re

class BleHelper:
    def uuid_filter(uuid):
        return re.sub(r'[^0-9abcdef]', '', uuid.lower())
    def to_camel_case(str):
        print('wip: toCamelCase')
    def to_snake_case(str):
        print('wip: toScakeCase')
