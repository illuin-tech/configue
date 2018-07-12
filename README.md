illuin-logging
==============

This repository contains some helpers to easily load configuration elements from files, it is based on `logging.config`.

The full API documentation is available in the [docs](./docs) folder.

# Usage

## Loading callables

This is useful if you want to insert a few environment variables.

```python
from illuin_config import load_config_from_dict

from my_project import settings


config = load_config_from_dict({
    "my_object": {
        "()": "path.to.callable",
        "my_argument": settings.MY_ARGUMENT,
        "my_other_argument": {
            "()": "path.to.other.callable"
        }
    }
})

```

In this example, `config["my_object"]` is the value returned by the callable defined by the property `()`.
It can be a class or a function.
The value is the path used to import the callable.

If you don't want to instantiate the object but still have a `"()"` key (useful for logging), you can use the value 
`\()` instead, it will be replaced with `"()"` automatically.


## Loading external variables

```python
from illuin_config import load_config_from_dict


config = load_config_from_dict({
    "my_object": {
        "()": "path.to.callable",
        "my_argument": "ext://my_other_project.settings.MY_ARGUMENT",
    }
})

```

When a value starts with `ext://`, the value will be imported from another module.


## Loading internal variables

```python
from illuin_config import load_config_from_dict


config = load_config_from_dict({
    "my_object": {
        "()": "path.to.callable",
        "my_argument": "my_value",
    },
    "my_other_object": "cfg://my_object"
})

```

When a value starts with `cfg://`, the value will be loaded from the same configuration dictionary
(useful for a DRY configuration).


## Loading configuration files

When the configuration becomes too complicated, you can store the dictionary in a `.json` or a `.yaml` file.

```python
from illuin_config import load_config_from_yaml_file, load_config_from_json_file, load_config_from_file


yaml_config = load_config_from_yaml_file("/path/to/my/file.yaml")
json_config = load_config_from_json_file("/path/to/my/file.json")
file_config = load_config_from_json_file("/path/to/my/file.json")  # This can be a json or a yaml file, the file extension
```
