Configue
========

A YAML parser with advanced functionalities to ease your application configuration.

# Who is this library for ?
This library is meant to be used in medium to large-scale applications, that have a lot of parameters to configure. 

Modular applications especially can greatly benefit from using `configue` to easily inject new modules.

# Installation

Run `pip install configue` to install from PyPI.

Run `pip install .` to install from sources.

# Usage

### Basic usage
This library uses [PyYAML](https://github.com/yaml/pyyaml) to parse the YAML files and return the file content.

```python
from configue import load_config_from_file


config = load_config_from_file("/path/to/yaml/file.yml")
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
from configue import load_config_from_file
from my_project import MyAwesomeClass
from my_project.my_module import MyOtherClass


my_instance = load_config_from_file("config.yml")
assert isinstance(my_instance, MyAwesomeClass)
assert my_instance.my_argument == "my_value"
assert isinstance(my_instance.my_other_argument, MyOtherClass)
```

Note that the instance is lazy-loaded if it is contained in a list or a dictionary, it is only created when the element
is called.

### Loading external variables

```yaml
# config.yml
my_argument: ext://my_project.my_module.my_variable
```

When a value starts with `ext://`, the value will be imported from the corresponding python module.


### Loading internal variables

```yaml
# config.yml
my_object:
    my_instance:
        (): my_project.MyClass
my_instance_shortcut: cfg://my_object.my_instance
```

When a value starts with `cfg://`, the value will be loaded from the same configuration file (useful for a DRY
configuration).

### Environment variables

If you want to load an environment variable in your YAML config file, you can use this syntax:
```yaml
# config.yml
my_key: ${var_name}
```
This will resolve as `"my_value"` if the environment variable `var_name` is set to this value.

If you need a default value in case the environment variable is not set:
```yaml
# config.yml
my_key: ${var_name-default}
```

You can insert this syntax in the middle of a string:
```yaml
# config.yml
my_key: prefix${var_name-default}suffix
```
This will resolve as `"prefixmy_value_suffix"` if the value is set, `"prefixdefaultsuffix"` if it is not.

If your value string starts with a special character (`%-.[]{},?:*&!|>\`), you need to quote it for the YAML parser.
Unfortunately, this breaks the detection of the `${}` pattern. You have to use this syntax instead:
```yaml
my_final_key: !env "{${var_name}}"
```
This will resolve as `"{my_value}"`.

In all those examples, if both the variable and the default value are not defined, the value is replaced by an empty
string, and then the field value is cast by the yaml loader (`""` becomes `None`, `"10"` becomes `10`, and `"true"`
becomes `True`).

#### Lists in environment variables
You can store a list in your environment variable, and use this syntax to split it on commas:
```yaml
# config.yml
my_list: !list ${my_var}
```
with `my_var=my_first_value,my_second_value`

This will resolve as `["my_value", "my_second_value"]`.


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
├── my_folder
    ├── my_file.txt
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
- var_1
- var_2
```

The path is resolved starting from the folder containing the parent yml file, this example will resolve to
`"my_import": [var_1, var_2]`

Do not start the import path with `/` as it will be treated as an absolute path instead.

You can use environment variables in your import path.

# Testing

Install the development dependencies with `pip install -r dev.requirements.txt`.

Run `python -m unitttest discover` to run the tests.

Run `pylint configue` to check the files linting.
