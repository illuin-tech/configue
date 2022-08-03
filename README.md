Configue
========

![CI](https://github.com/illuin-tech/configue/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/illuin-tech/configue/branch/master/graph/badge.svg)](https://codecov.io/gh/illuin-tech/configue)

A YAML parser with advanced functionalities to ease your application configuration.

# Who is this library for ?
This library is meant to be used in medium to large-scale applications, that have a lot of parameters to configure. 

Modular applications especially can greatly benefit from using `configue` to easily inject new modules.

# Installation

Run `pip install configue` to install from PyPI.

Run `pip install .` to install from sources.

This project follows the (Semantic Versioning Specification)[https://semver.org/].
All breaking changes are described in the [Changelog](CHANGELOG.md). 

# Usage

### Basic usage
This library uses [PyYAML](https://github.com/yaml/pyyaml) to parse the YAML files and return the file content.

```python
import configue


config = configue.load("/path/to/yaml/file.yml")
```


### Loading a sub path
If you are not interested in loading the whole file, you can only load a subpath:
```yaml
# config.yml
some_key:
  some_list:
    - first_item
    - second_item:
        item_key: item_value

not_loaded_key: not_loaded_value
```

```python
import configue

config = configue.load("config.yml", "some_key.some_list.1.item_key")
assert config == "item_value"
```

### Instantiating classes

Use `()` in your YAML files to instantiate classes:
```yaml
# config.yml
(): "my_project.MyAwesomeClass"
my_argument: "my_value"
my_other_argument:
  (): "my_project.my_module.MyOtherClass"
```

```python
import configue
from my_project import MyAwesomeClass
from my_project.my_module import MyOtherClass


my_instance = configue.load("config.yml")
assert isinstance(my_instance, MyAwesomeClass)
assert my_instance.my_argument == "my_value"
assert isinstance(my_instance.my_other_argument, MyOtherClass)
```


### Loading external variables

```yaml
# config.yml
my_argument: !ext my_project.my_module.my_variable
```

When using the `!ext` tag, the value will be imported from the corresponding python module.


### Loading internal variables

```yaml
# config.yml
my_object:
    my_instance:
        (): my_project.MyClass
my_instance_shortcut: !cfg my_object.my_instance
```

When using the `!cfg` tag, the value will be loaded from the same configuration file (useful for a DRY configuration).

### Environment variables

If you want to load an environment variable in your YAML config file, you can use this syntax:
```yaml
# config.yml
my_key: ${VAR_NAME}
```
This will resolve as `"my_value"` if the environment variable `VAR_NAME` is set to this value.

If you need a default value in case the environment variable is not set:
```yaml
# config.yml
my_key: ${VAR_NAME-default}
```

You can insert this syntax in the middle of a string:
```yaml
# config.yml
my_key: prefix${VAR_NAME-default}suffix
```
This will resolve as `"prefixmy_value_suffix"` if the value is set, `"prefixdefaultsuffix"` if it is not.

If your environment variable resolves to a yaml value, it will be cast (unless you are using quotes):
```yaml
# config.yml
my_key: ${VAR_NAME}
my_quoted_key: "${VAR_NAME}"
```
This will resolve as `True` if the value is set to `true`, `yes` or `y`, `None` if the value is set to `~` or `null`.


### Relative paths

If you want to expand a relative path in your YAML config file:

````yaml
# config.yml
my_path: !path my_folder/my_file.txt  
````
Assuming your file structure looks like this:
```
root/
├── config.yml
└── my_folder
    └── my_file.txt
```

The path is resolved starting from the folder containing the parent yml file, this example will resolve to
`/root/my_folder/my_file.txt`

Do not start the path with `/` as it will be treated as an absolute path instead.

You can use environment variables in your file path.

### Importing other files

You can import another file directly in your YAML config file:

````yaml
# config.yml
my_import: !import my_folder/my_other_config.yml
````

```yaml
# my_other_config.yml
some_key:
    - var_1
    - var_2
```

By default, the path is resolved starting from the folder containing the parent yml file, this example will resolve to
`"my_import": {"some_key": [var_1, var_2]}`

If you want to import only a section of the file, use the path in the tag suffix `!import:some_key.0`

Do not start the import path with `/` as it will be treated as an absolute path instead.

You can use environment variables in your import path.

### Logging configuration

You can load the logging configuration for your application by using the `logging_config_path` parameter:
```yaml
# config.yml
logging_config:
  version: 1
  handlers:
    console:
      class : logging.StreamHandler
      stream  : ext://sys.stdout
    custom_handler:
      \(): my_app.CustomHandler
      some_param: some_value
      level: ERROR
  root:
    level: INFO
    handlers:
      - console

app_config:
  some_key: some_value

not_loaded_key: not_loaded_value
```

```python
import logging

import configue

app_config = configue.load("config.yml", "app_config", logging_config_path="logging_config")
assert app_config == {"some_key": "some_value"}

logger = logging.getLogger(__name__)
logger.info("Hello world!")  # Uses the console handler
```

The logging configuration should follow the format of `logging.config.dictConfig`
(check [the documentation](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema) for more
details).
Make sure to escape the constructors with `\()` instead of `()` for handlers, formatters and filters.


# Testing

Install the development dependencies with `pip install -r dev.requirements.txt`.

Run `python -m unitttest discover` to run the tests.

Run `pylint configue` to check the files linting.
