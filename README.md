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

When the configuration becomes too complicated, you can store the dictionary in a `.yaml` file.

```python
from illuin_config import load_config_from_yaml_file, load_config_from_file


yaml_config = load_config_from_yaml_file("/path/to/my/file.yaml")
# This can be a YAML or a JSON (deprecated) file, the file extension is used to determine the file type
file_config = load_config_from_file("/path/to/my/file.yaml")
```

## Using YAML templating
These syntax helpers are only available when loading the configuration from a YAML file (not JSON or a dictionary).

You can use only one tag at a time (you can't put a path and and environment variable in the same value).

### Environment variables

If you want to load an environment variable in your YAML config file, you can use this syntax:
```yaml
my_key: ${var_name}
```
This will resolve as `"my_value"` if the environment variable `var_name` is set to this value.

If you need a default value in case the environment variable is not set:
```yaml
my_key: ${var_name-default}
```

You can insert this syntax in the middle of a string:
```yaml
my_key: prefix${var_name-default}suffix
```
This will resolve as `"prefixdefault_valuesuffix"` if the value is not set, `"prefixmy_value_suffix"` if it is.

If your value string starts with a special character (`%-.[]{},?:*&!|>\`), you need to quote it for the YAML parser.
Unfortunately, this breaks the detection of the `${}` pattern. You have to use this syntax instead:
```yaml
my_final_key: !env "{${var_name}}"
```
This will resolve as `{my_value}`.

In all those examples, if both the variable and the default value are not defined, the value is replaced by `""`.

### Relative paths

If you want to expand a relative path in your YAML config file:

````yaml
my_path: !path my_folder/my_file.txt  
````
This will resolve to "/path/to/config.yml/../my_folder/my_file.txt"

Do not start the relative path by `/` as it will be treated as an absolute path instead.

````yaml
my_path: !path /my_folder/my_file.txt  # This will resolve to "/my_folder/my_file.txt" 
````
