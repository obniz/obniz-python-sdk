from .obniz_system_methods import ObnizSystemMethods


class ObnizUIs(ObnizSystemMethods):
    def __init__(self, id, options):
        super().__init__(id, options)

    def _is_valid_obniz_id(self, string):
        if type(string) is not str or len(string) < 8:
            return False

        string = string.replace("-", "")

        try:
            int(string)
        except ValueError:
            return False

        return True

    def wsconnect(self, desired_server=None):
        if not self._is_valid_obniz_id(self.id):
            self.error("invalid obniz id")
            return

        super().wsconnect(desired_server)
