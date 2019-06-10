import json
import attrdict

class ObnizUtil:
    @classmethod
    def _key_filter(cls, params, keys):
        filterd_params = {}
        if type(params) not in [dict, attrdict.default.AttrDefault]:
            return filterd_params

        for key in [key for key in params.keys() if key in keys]:
            filterd_params[key] = params[key]

        return filterd_params

    @classmethod
    def _required_keys(cls, params, keys):
        if type(params) not in [dict, attrdict.default.AttrDefault]:
            return keys[0]

        for key in keys:
            if key not in params:
                return key

        return None

    @classmethod
    def data_array2string(cls, data):
        return "".join([chr(d) for d in data])

    @classmethod
    def string2data_array(cls, string):
        return [ord(c) for c in list(string)]

    @classmethod
    def json_dumps(cls, obj):
        return json.dumps(obj, default=_default)


def _default(obj):
    if hasattr(obj, "to_json"):
        return obj.to_json()
    raise TypeError(repr(obj) + " is not JSON serializable")
