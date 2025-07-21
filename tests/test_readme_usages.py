from dictpress import flatten_dict, merge, unflatten_dict


def test_flatten_dict_example():
    """Test the flatten_dict example from README."""
    data = {"a": {"b": {"c": 1}}, "x": 2}
    flattened = flatten_dict(data)
    expected = {"a.b.c": 1, "x": 2}
    assert flattened == expected


def test_unflatten_dict_example():
    """Test the unflatten_dict example from README."""
    flattened = {"a.b.c": 1, "x": 2}
    nested = unflatten_dict(flattened)
    expected = {"a": {"b": {"c": 1}}, "x": 2}
    assert nested == expected


def test_merge_example():
    """Test the merge example from README."""
    base = {"a": {"b": 1}, "c": 2}
    update = {"a": {"d": 3}, "e": 4}
    merged = merge(base, update)
    expected = {"a": {"b": 1, "d": 3}, "c": 2, "e": 4}
    assert merged == expected


def test_round_trip():
    """Test that flatten -> unflatten preserves original structure."""
    original = {"a": {"b": {"c": 1}}, "x": 2}
    flattened = flatten_dict(original)
    restored = unflatten_dict(flattened)
    assert restored == original


def test_merge_precedence():
    """Test that merge gives precedence to update values."""
    base = {"a": {"b": 1, "c": 2}}
    update = {"a": {"b": 999}}  # Should override base value
    merged = merge(base, update)
    expected = {"a": {"b": 999, "c": 2}}
    assert merged == expected


def test_empty_dicts():
    """Test edge cases with empty dictionaries."""
    assert flatten_dict({}) == {}
    assert unflatten_dict({}) == {}
    assert merge({}, {"a": 1}) == {"a": 1}
    assert merge({"a": 1}, {}) == {"a": 1}
