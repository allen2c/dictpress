# dictpress

Simple dictionary manipulation utilities for Python.

## Installation

```bash
pip install dictpress
```

## Usage

```python
from dictpress import flatten_dict, unflatten_dict, merge

# Flatten nested dictionaries
data = {"a": {"b": {"c": 1}}, "x": 2}
flattened = flatten_dict(data)
# {"a.b.c": 1, "x": 2}

# Unflatten back to nested structure
nested = unflatten_dict(flattened)
# {"a": {"b": {"c": 1}}, "x": 2}

# Deep merge dictionaries
base = {"a": {"b": 1}, "c": 2}
update = {"a": {"d": 3}, "e": 4}
merged = merge(base, update)
# {"a": {"b": 1, "d": 3}, "c": 2, "e": 4}
```

## API

### `flatten_dict(data: dict) -> dict`

Flatten nested dictionary into single-level with dot notation keys.

### `unflatten_dict(data: dict) -> dict`

Convert flattened dictionary back to nested structure.

### `merge(data: dict, update: dict) -> dict`

Deep merge two dictionaries. Values from `update` take precedence.
