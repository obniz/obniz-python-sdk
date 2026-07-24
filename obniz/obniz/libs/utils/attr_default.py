class AttrDefault(dict):
    """In-repo replacement for the abandoned attrdict package's AttrDefault.

    A dict whose keys are also readable/writable as attributes, and whose
    missing keys yield default_factory() (stored, like collections.defaultdict)
    instead of raising. Parts rely on all three behaviors, e.g.
    ``self.params.mode = self.params.mode or 'master'``.
    """

    def __init__(self, default_factory=bool, items=None):
        super().__init__(items if items is not None else {})
        object.__setattr__(self, "_default_factory", default_factory)

    def __getitem__(self, key):
        if key not in self:
            default = self._default_factory()
            super().__setitem__(key, default)
            return default
        return super().__getitem__(key)

    def __getattr__(self, key):
        if key.startswith("__"):
            raise AttributeError(key)
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)

    def get(self, key, default=None):
        # do not auto-create on .get(), matching plain dict semantics
        if key in self:
            return dict.__getitem__(self, key)
        return default
