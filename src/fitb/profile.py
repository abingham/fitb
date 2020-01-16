class Profile:
    def __init__(self):
        self._options = set()
        self._extension_points = _ExtensionPoints()

    def add_option(self, option):
        self._options.add(option)

    def options(self):
        yield from self._options
        for ep in self.extension_points:
            yield from ep.config_options()

    @property
    def extension_points(self):
        return self._extension_points


class _ExtensionPoints:
    def __init__(self):
        self._eps = {}

    def add(self, extension_point):
        self._eps[extension_point.name] = extension_point

    def __getitem__(self, name):
        return self._eps[name]

    def __iter__(self):
        return iter(self._eps.values())
