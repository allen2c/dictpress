import typing

from benedict import benedict


def flatten_dict(data: dict) -> dict:
    """
    Flatten a nested dictionary into a single-level dict.
    Keys are joined with dots (e.g., 'a.b.c' for nested['a']['b']['c']).
    """
    return dict(
        typing.cast(
            benedict, benedict(data, keypath_separator="\x1f").flatten(separator=".")
        )
    )


def unflatten_dict(data: dict) -> dict:
    """
    Convert a flattened dictionary back to its original nested structure.
    Reverses the operation performed by flatten_dict().
    """
    return dict(
        typing.cast(
            benedict, benedict(data, keypath_separator="\x1f").unflatten(separator=".")
        )
    )


def merge(data: dict, update: dict) -> dict:
    """
    Merge two dictionaries with deep merging support.
    Values from 'update' take precedence over 'data' for conflicting keys.
    """
    out = flatten_dict(data)
    out.update(flatten_dict(update))
    return unflatten_dict(out)
