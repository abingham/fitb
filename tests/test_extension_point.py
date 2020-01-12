from report_generator import extension_points
import pytest


def test_names():
    reporters, generators = extension_points()
    assert reporters.name == 'reporters'
    assert generators.name == 'generators'


def test_default_config():
    reporters, generators = extension_points()

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


def test_get_names():
    reporters, generators = extension_points()

    reporters.activate(reporters.default_config())
    assert sorted(reporters.names()) == ['all-caps', 'lower']

    generators.activate(generators.default_config())
    assert sorted(generators.names()) == ['calm', 'frantic']


def test_get_names_prior_to_activation_is_empty():
    reporters, generators = extension_points()
    assert sorted(reporters.names()) == []
    assert sorted(generators.names()) == []


def test_get_by_name():
    reporters, generators = extension_points()

    reporters.activate(reporters.default_config())
    for name in reporters.names():
        reporters[name]

    generators.activate(generators.default_config())
    for name in generators.names():
        generators[name]


def test_get_name_raises_KeyError_on_missing_name():
    reporters, generators = extension_points()

    reporters.activate(reporters.default_config())
    with pytest.raises(KeyError):
        reporters['no-such-reporter']

    generators.activate(generators.default_config())
    with pytest.raises(KeyError):
        reporters['no-such-generators']
