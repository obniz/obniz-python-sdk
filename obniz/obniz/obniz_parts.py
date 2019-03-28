from attrdict import AttrDefault

from .obniz_connection import ObnizConnection
from .libs.utils.util import ObnizUtil

_parts = {}

class ObnizParts(ObnizConnection):
    def __init__(self, id, options):
        super().__init__(id, options)
    
    def _parts(self):
        return _parts
    
    @staticmethod
    def parts_registrate(*args):
        if (len(args) == 1):
            _parts[args[0].info()["name"]] = args[0]
        elif (len(args) == 2):
            _parts[args[0]] = args[1]
        else:
            pass
    
    @staticmethod
    def parts(name):
        if name not in _parts:
            raise Exception("unknown parts [" + name + "]")
        return _parts[name]
    
    def wired(self, partsname, param=None):
        parts = ObnizParts.parts(partsname)
        if not parts:
            raise Exception("No such a parts [" + partsname + "] found")
        
        if parts.keys:
            if parts.required_keys:
                err = ObnizUtil._required_keys(param, parts.required_keys)
                if err:
                    raise Exception(
                        partsname + " wired param '" + err + "' required, but not found "
                    )
        
            parts.params = AttrDefault(bool, ObnizUtil._key_filter(param, parts.keys))
        
        parts.obniz = self
        parts.wired(parts.obniz)
        if parts.keys or parts.io_keys:
            keys = parts.keys if hasattr(parts, "keys") else parts.io_keys
            display_parts_name = parts.display_name if hasattr(parts, "display_name") else partsname
            io_names = {}

            for key in keys:
                pin_name = key
                io = param[pin_name] if pin_name in param else None
                if self.is_valid_io(io):
                    if hasattr(parts, "display_io_names") and parts.display_io_names[pin_name]:
                        pin_name = parts.display_io_names[pin_name]
                    io_names[io] = pin_name
            
            self.display.set_pin_names(display_parts_name, io_names)
        
        return parts
