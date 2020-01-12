from string import printable

import hypothesis.strategies as st
import pytest
from hypothesis import assume, given

from fitb.utilities import merge

# config = st.deferred(lambda: st.dictionaries(st.text(), (st.integers() | config)))
config = st.recursive(st.dictionaries(st.text(printable), st.integers()),
                      lambda children: st.dictionaries(st.text(printable), children),
                      max_leaves=5)


def paths(config):
    for name, value in config.items():
        if not isinstance(value, dict):
            yield (name,)
        else:
            for path in paths(value):
                yield (name,) + path


def get(config, path):
    assert len(path) > 0
    sub = config[path[0]]
    if len(path) > 1:
        assert isinstance(sub, dict)
        return get(sub, path[1:])
    return sub


def test_merge_empty():
    assert merge({}, {}) == {}


@given(config)
def test_empty_second(config):
    assert merge(config, {}) == config


@given(config)
def test_empty_first(config):
    assert merge({}, config) == config


@given(config, config)
def test_src_always_in_output(dest, src):
    try:
        merged = merge(dest, src)
    except ValueError:
        assume(False)

    src_paths = set(paths(src))
    merged_paths = set(paths(merged))

    for path in src_paths:
        assert path in merged_paths
        assert get(merged, path) == get(src, path)


@given(config, config)
def test_dest_in_merged_if_no_overwritten(dest, src):
    try:
        merged = merge(dest, src)
    except ValueError:
        assume(False)

    dest_paths = set(paths(dest))
    src_paths = set(paths(src))
    merged_paths = set(paths(merged))

    for path in dest_paths:
        if path not in src_paths:
            assert path in merged_paths
            assert get(merged, path) == get(dest, path)


def test_incompatible_structures_raise_ValueError():
    with pytest.raises(ValueError):
        merge({'': 0}, {'': {}})

    with pytest.raises(ValueError):
        merge({'': {}}, {'': 0})


def test_merge_returns_new_dict():
    dest = {}
    src = {}
    m = merge(dest, src)
    assert m is not dest
    assert m is not src
