import pytest


def test_names(reporters, generators):
    assert reporters.name == 'reporters'
    assert generators.name == 'generators'


# TODO: Test config_options()

def test_iterate(reporters, generators):
    assert sorted([e.name for e in reporters]) == ['all-caps', 'lower']
    assert sorted([e.name for e in generators]) == ['calm', 'frantic']


def test_get_name_raises_KeyError_on_missing_name(reporters, generators):
    with pytest.raises(KeyError):
        reporters['no-such-reporter']
    with pytest.raises(KeyError):
        reporters['no-such-generators']
