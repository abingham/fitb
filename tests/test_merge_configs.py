from fitb import build_default_config, merge, Option


def test_merge_simple():
    spec = [(('my-app', 'screen'), Option('width', 'Width of screen', 100)),
            (('my-app', 'screen'), Option('height', 'Height of screen', 200))]

    config = build_default_config(spec)

    merge(dest=config, src={'my-app': {'screen': {'width': 400}}})

    assert config == {
        'my-app': {
            'screen': {
                'width': 400,
                'height': 200,
            }
        }
    }


def test_merge_into_empty():
    config = {}
    update = {'foo': {'bar': 1234}}
    merge(dest=config, src=update)

    assert config == update
    assert config is not update


def test_merge_from_empty():
    spec = [(('my-app', 'screen'), Option('width', 'Width of screen', 100)),
            (('my-app', 'screen'), Option('height', 'Height of screen', 200))]

    baseline = build_default_config(spec)

    config = build_default_config(spec)
    merge(dest=config, src={})

    assert config == baseline
    assert config is not baseline
