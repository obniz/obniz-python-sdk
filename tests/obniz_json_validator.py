import os.path

from jsonschema import Draft4Validator, RefResolver
import yaml


class ObnizJsonValidator:
    # def __init__(self):
    #     self.use_commands = {}s
    #     self.cache = {}

    def request_validate(self, request_json, type):
        valid = self._validate(request_json, "request")
        if not valid:
            return {"valid": False, "errors": ["json are valid for no command"]}
        else:
            # self.use_commands[type] = self.use_commands[type] or []
            # self.use_commands[type].push(commands[0])
            return {"valid": True, "errors": []}

    def response_validate(self, request_json, type):
        valid = self._validate(request_json, "response")
        if not valid:
            return {"valid": False, "errors": ["json are valid for no command"]}
        else:
            # self.use_commands[type] = self.use_commands[type] or []
            # self.use_commands[type].push(commands[0])
            return {"valid": True, "errors": []}

    def _validate(self, json, type):
        class Resolver(RefResolver):
            def __init__(self):
                super().__init__("", None)

            def resolve_remote(self, uri):
                if uri == "/obnizId":
                    uri = ""
                uri = "./json_schema" + uri
                if os.path.isdir(uri):
                    uri += "/index"
                uri += ".yml"

                if not os.path.isfile(uri):
                    uri = "./json_schema/index.yml"

                with open(uri) as f:
                    result = yaml.load(f, Loader=yaml.FullLoader)

                if self.cache_remote:
                    self.store[uri] = result
                return result

        with open("./json_schema/" + type + "/index.yml") as f:
            schema = yaml.load(f, Loader=yaml.FullLoader)

        Draft4Validator(schema, resolver=Resolver()).validate(json)

        return True


obniz_json_validator = ObnizJsonValidator()
