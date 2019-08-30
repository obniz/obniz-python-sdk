from pyee import AsyncIOEventEmitter
import semver

class BleSecurity:
    def __init__(self, obniz):
        self.obniz = obniz
        self.emitter = AsyncIOEventEmitter()

    def set_mode_level(self, mode, level):
        auth = None
        keys = None
        indicate_security_level = None

        if mode == 1:
            if level == 1:
                auth = []
                indicate_security_level = 0
                keys = ['LTK', 'IRK']
            elif level == 2:
                auth = ['bonding']
                indicate_security_level = 2
                keys = ['LTK', 'IRK']
            elif level == 3:
                # TODO
                # auth = ['bonding','mitm']
                # indicateSecurityLevel = 3
                # keys = ['LTK', 'IRK']
                pass
        elif mode == 2:
            if level == 1:
                # TODO
                # auth = []
                # keys = ['LTK', 'IRK','CSRK']
                pass
            elif level == 2:
                # TODO
                # auth = ['bonding']
                # keys = ['LTK', 'IRK','CSRK']
                pass
        
        if (not auth and not indicate_security_level and not keys):
            self.set_auth(auth)
            self.set_indicate_security_level(indicate_security_level)
            self.set_enable_key_types(keys)
        else:
            msg = (
                "BLE security mode {}, ".format(mode) + 
                "level {} is not available.".format(level)
            )
            self.obniz.error(msg)
            raise Exception(msg)
    
    def check_introduced_firmware(self, introduced_version, function_name):
        res = semver.match(self.obniz.firmware_ver, "<=" + introduced_version)
        if res:
            msg = (
                "{} is available ".format(function_name) +
                "on obniz firmware {}.".format(introduced_version) +
                "(your obniz firmware version is " +
                "{})".format(self.obniz.firmware_ver)
            )
            self.obniz.error(msg)
            raise Exception(msg)

    def set_auth(self, auth_types):
        self.check_introduced_firmware('1.1.0', 'set_auth')
        if type(auth_types) is not list:
            auth_types = [auth_types]
        send_types = [
            elm.lower() for elm in auth_types if elm.lower() in ['mitm', 'secure_connection', 'bonding']
        ]
        if len(send_types) != len(auth_types):
            raise Exception("unknown auth type")
        
        self.obniz.send({
            "ble": {
                "security": {
                    "auth": send_types
                }
            }
        })

    def set_indicate_security_level(self, level):
        self.check_introduced_firmware('1.1.0', 'set_indicate_security_level')

        if type(level) is not int:
            raise Exception("unknown security level: " + str(level))
        
        self.obniz.send({
            "ble": {
                "security": {
                    "indicate_security_level": level
                }
            }
        })

    def set_enable_key_types(self, key_types):
        self.check_introduced_firmware('1.1.0', 'set_enable_key_types')
        if type(key_types) is not list:
            key_types = [key_types]
        send_types = [
            elm.lower() for elm in auth_types if elm.lower() in ['ltk', 'csrk', 'irk']
        ]
        if len(send_types) != len(key_types):
            raise Exception("unknown key type")
        
        self.obniz.send({
            "ble": {
                "security": {
                    "key": {
                        "type": send_types
                    }
                }
            }
        })
    
    def set_key_max_size(self, size):
        self.check_introduced_firmware('1.1.0', 'set_key_max_size')
        if type(size) is not int:
            raise Exception("please provide key size in number")
        self.obniz.send({
            "ble": {
                "security": {
                    "key": {
                        "max_size": size
                    }
                }
            }
        })

    def clear_bonding_devices_list(self):
        self.obniz.send({
            "ble": {
                "security": {
                    "devices": {
                        "clear": True
                    }
                }
            }
        })
    
    def onerror(self, *args):
        pass # dummy
    
    def notify_from_server(self, notify_name, params):
        if notify_name == "onerror":
            self.onerror(params)