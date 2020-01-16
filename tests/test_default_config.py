from itertools import chain
from fitb import ExtensionPoint, build_default_config


def test_default_config(reporters: ExtensionPoint, generators: ExtensionPoint):
    config = build_default_config(
        chain(
            reporters.config_options(),
            generators.config_options()
        ))

    assert config == {
        'reporters': {
            'all-caps': {
                'loud': False
            },
        },
    }
