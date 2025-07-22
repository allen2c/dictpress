import pathlib
import typing

from benedict import benedict

__version__ = pathlib.Path(__file__).parent.joinpath("VERSION").read_text().strip()
__all__ = ["flatten_dict", "unflatten_dict", "merge", "get_deep", "set_deep"]


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


def get_deep(
    data: dict, key: str, default: typing.Any | None = None
) -> typing.Any | None:
    """
    Get a value from nested dictionary using dot notation or suffix matching.
    Searches for exact key match or keys ending with '.{key}'.
    Returns the found value or default if not found.
    """
    for k, v in flatten_dict(data).items():
        if k == key:
            return v
        if k.endswith(f".{key}"):
            return v
    return default


def set_deep(
    data: dict, key: str, value: typing.Any
) -> dict:  # key is a dot-separated path, return new dict
    """
    Set a value in nested dictionary using dot-separated path notation.
    Creates a new dictionary with the specified value at the given path.
    Does not modify the original dictionary.
    """

    updater = {key: value}
    return merge(data, updater)
