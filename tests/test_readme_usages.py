from dictpress import flatten_dict, get_deep, merge, set_deep, unflatten_dict


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


def test_get_deep_example():
    """Test the get_deep examples from README."""
    data = {"user": {"profile": {"name": "Alice", "age": 30}}}

    # Suffix match
    name = get_deep(data, "name")
    assert name == "Alice"

    # Exact match
    age = get_deep(data, "user.profile.age")
    assert age == 30

    # Default value
    missing = get_deep(data, "missing", "default")
    assert missing == "default"


def test_get_deep_case_sensitive():
    """Test the case_sensitive parameter in get_deep."""
    data = {"User": {"Profile": {"Name": "Alice", "AGE": 30}}}

    # Case-sensitive (default) - should not find lowercase keys
    assert get_deep(data, "name") is None
    assert get_deep(data, "age") is None
    assert get_deep(data, "user.profile.name") is None

    # Case-sensitive (explicit) - should not find lowercase keys
    assert get_deep(data, "name", case_sensitive=True) is None
    assert get_deep(data, "age", case_sensitive=True) is None

    # Case-insensitive - should find keys regardless of case
    assert get_deep(data, "name", case_sensitive=False) == "Alice"
    assert get_deep(data, "age", case_sensitive=False) == 30
    assert get_deep(data, "user.profile.name", case_sensitive=False) == "Alice"

    # Exact case matches should work in both modes
    assert get_deep(data, "Name") == "Alice"
    assert get_deep(data, "Name", case_sensitive=False) == "Alice"


def test_set_deep_example():
    """Test the set_deep example from README."""
    data = {"a": 1}
    result = set_deep(data, "user.name", "Bob")
    expected = {"a": 1, "user": {"name": "Bob"}}
    assert result == expected

    # Original data unchanged
    assert data == {"a": 1}


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


def test_get_deep_edge_cases():
    """Test get_deep edge cases."""
    data = {"a": {"b": {"c": 1}}}

    # Non-existent key returns None by default
    assert get_deep(data, "missing") is None

    # Multiple suffix matches - returns first found
    data_multi = {"x": {"name": "first"}, "y": {"name": "second"}}
    result = get_deep(data_multi, "name")
    assert result in ["first", "second"]  # Either is valid


def test_set_deep_nested():
    """Test set_deep with deeply nested paths."""
    data = {}
    result = set_deep(data, "a.b.c.d", "deep")
    expected = {"a": {"b": {"c": {"d": "deep"}}}}
    assert result == expected
