import pytest


def test_names(reporters, generators):
    assert reporters.name == 'reporters'
    assert generators.name == 'generators'


def test_default_config(reporters, generators):
    assert reporters.default_config() == {
        'all-caps': {
            'loud': False
        },
        'lower': {}
    }

    assert generators.default_config() == {
        'calm': {},
        'frantic': {}
    }


def test_iterate(reporters, generators):
    assert sorted(reporters) == ['all-caps', 'lower']
    assert sorted(generators) == ['calm', 'frantic']


def test_get_by_name(reporters, generators):
    for name in reporters:
        reporters[name]
    for name in generators:
        generators[name]


def test_get_name_raises_KeyError_on_missing_name(reporters, generators):
    with pytest.raises(KeyError):
        reporters['no-such-reporter']
    with pytest.raises(KeyError):
        reporters['no-such-generators']
