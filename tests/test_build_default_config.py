from fitb import build_default_config, Option


def test_empty_spec():
    config = build_default_config([])
    assert config == {}


def test_simple_tree():
    spec = [(('my-app', 'screen'), Option('width', 'Width of screen', 100)),
            (('my-app', 'screen'), Option('height', 'Height of screen', 200))]

    config = build_default_config(spec)

    assert config == {
        'my-app': {
            'screen': {
                'width': 100,
                'height': 200,
            }
        }
    }
