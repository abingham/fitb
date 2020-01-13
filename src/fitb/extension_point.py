"""Define a simple system of extension-points and extensions.

An extension-point represents a point in a program that can be extended. It comprises a name and a collection of
extensions at that point. Each extension on an extension-point provides a specific "implementation" for that
extension-point.

Extensions themselves comprise a name, a description, a sequence of configurable options, and a method for "activating"
them. This activation produces the object that actually embodies the implementation of the extension.
"""

import logging
from fitb.utilities import merge

from .extension import Extension

log = logging.getLogger()


class ExtensionPoint:
    """A named point in a program that can be extended.
    """

    def __init__(self, name):
        self._name = name
        self._extensions = {}

    @property
    def name(self):
        "The name of the extension point."
        return self._name

    def add(self, name, description, activate, config_options=()):
        """Add an extension to the point.
        """
        extension = Extension(
            name=name,
            description=description,
            config_options=config_options,
            activate=activate)

        if extension.name in self._extensions:
            raise ValueError(
                'Extension {} already in {}'.format(extension.name, self))

        self._extensions[extension.name] = extension

    def activate(self, name, config):
        """Activate an extension.

        Args:
            name: The name of the extension to activate.
            config: The full config dict.

        Returns:
            The activate extension object (i.e. as returned from the extension on activation).

        Raises:
            KeyError: There is no extension named `name`.
        """
        return self._extensions[name].activate(
            config,
            config.get(self.name, {}).get(name, {}))

    def default_config(self):
        """The complete default configuration dict for this point.

        This examines each extension point and constructs a config containing all of the
        default values for their configuration options.

        The config is structured like this::

            {
                extension_point_name: {
                    extension_name: { . . . default extension config . . . },
                    . . .
                }
            }
        """
        config = {}
        for extension in self._extensions.values():
            config = merge(
                config,
                {
                    extension.name: {
                        option.name: option.default
                        for option in extension.config_options
                    }
                }
            )
        return config

    def __getitem__(self, name):
        """Get the extension object with the given name.
        
        Returns: An Extension instance.

        Raises:
            KeyError: There is no extension with that name.
        """
        return self._extensions[name]

    def __iter__(self):
        "Iterable of extension names."
        return iter(self._extensions)

    def __repr__(self):
        return "ExtensionPoint(name='{}')".format(self.name)
