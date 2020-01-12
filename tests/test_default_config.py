from report_generator import extension_points
from fitb.utilities import default_config


def test_default_config():
    assert default_config(*extension_points()) == {
        'reporters': {
            'all-caps': {
                'loud': False
            },
            'lower': {}
        },
        'generators': {
            'calm': {},
            'frantic': {}
        }
    }
