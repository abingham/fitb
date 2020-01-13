from fitb.utilities import default_config


def test_default_config(reporters, generators):
    assert default_config(reporters, generators) == {
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
