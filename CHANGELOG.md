# Changelog
## Unreleased
## 4.1.1
### Fixes
- Fixed loading `!import` or `!cfg` tags in a `!cfg` tag

## 4.1.0
### Features
- Added a `logging_config_path` keyword parameter to `configue.load` to set up a logging configuration while loading a
configuration file

## 4.0.1
### Fixes
- Loading a null `!path` will now return `None` instead of raising an Exception

## 4.0.0
### Breaking changes
- The `!env` tag has been removed, environment variables can now be loaded anywhere
- The `cfg://` syntax has been replaced with `!cfg path.to.value`
- `!cfg` now redirects to a path in the current file (instead of the first loaded file)
  - Use `!import` to load a path in another file
- The `ext://module.submodule.object` syntax has been replaced with `!ext module.submodule.object`
- Replaced `load_config_from_file` with a `configue.load` function, which is now the main entrypoint of the library
  - use `configue.load("/path/to/file.yml")` to load a file
  - use `configue.load("/path/to/file.yml", "path.to.section")` to load only a section of a file
  - loading a path in a file recursively loads all children (replaced the lazy-loading with path loading),
  see README for more details
- Removed the `load_config_from_dict` function
- The `!list` tag has been removed, set your environment variable to `[value_1, value_2]` instead

### Migration guide
- Remove all `!env` tags
- Remove all `!list` tags, and replace your environment variables from `value1,value2` to `[value1,value2]`
- Replace `ext://path.to.load` with `!ext path.to.load`
- If you are using `!import` to import a file containing values with `cfg://path.to.load`, replace the `cfg://...` with
`!import:path/to/root/file.yml path.to.load`
- Replace `cfg://path.to.load` with `!cfg path.to.load`
- Replace `configue.load_config_from_file(...)` with `configue.load(...)`
- Replace `configue.load_config_from_file(...)["path"]["to"]["load"]` with `configue.load(..., "path.to.load")`

### Features
- The `!import` tag can now specify the path to load in the other file, with the syntax:
`!import:path.to.load path/to/file.yml`
- Dictionaries and lists are now JSON dumpable and picklable

### Fixes
- Removed warning about missing environment variables from unloaded paths


## 3.0.5
### Enhancements
- Added Python 3.10 support
- Updated PyYAML dependency version


## 3.0.4
### Enhancements
- Added Python 3.9 support

### Fixes
- Fixed DeprecationWarning on collections import


## 3.0.3
### Fixes
- Fixed key errors when loading `cfg://` paths from file


## 3.0.2
### Fixes
- Fixed top-level object loading


## 3.0.1
### Fixes
- Fixed PyPI package description


## 3.0.0
### Breaking changes
- Renamed into `configue`
- Removed json loading


## 2.4.2
### Enhancements
- Updated dependency: `pyyaml` to `5.1`


## 2.4.1
### Fixes
- Fixed warnings for missing environment variables appearing when a default was set


## 2.4.0
### Features
- Added a warning log when an environment variable is missing


## 2.3.0
### Features
- Using `**kwargs`, `.items()` or `.values()` with a dictionary created with the `ConfigLoader` now converts the value

### Fixes
- An error log has been added when a class instantiation fails


## 2.2.3
### Fixes
- `!path` and `!import` now work as expected when used after importing a file from another folder


## 2.2.2
### Fixes
- `~` paths are correctly expanded when used with `!path` in yaml files


## 2.2.1
### Fixes
- Emojis are now supported in yaml files


## 2.2.0
### Features
- Environment variables can now contain lists in YAML files, use `!list ${my_var}` to create a python list when loading
the file.


## 2.1.0
### Features
- Environment variables can now be inserted in `!path` values
- Values that contain environment variables are now cast into strings, booleans, ints or floats
- You can use `!import` to concatenate files

### Fixes
- Multiple environment variables can now be inserted in the same value


## 2.0.0
### Breaking changes
- Removed escaped callable syntax `\()`

### Fixes
- Fixed a bug where tuples where not converted on access


## 1.3.1
### Fixes
- Fixed a bug that prevented accessing objects properties with `cfg://`


## 1.3.0
### Features
- Added environment variables templating with `${var_name-default}` when loading from YAML files
- Added path completion with `!path folder/my_file.txt` when loading from YAML files
(prepends the absolute path to the folder containing the configuration file)

### Deprecated
- `load_config_from_json` has been deprecated in favor of `load_config_from_yaml`
- `load_config_from_file` has been deprecated when using JSON files (use YAML files instead)


## 1.2.0
### Features
- Added callable list support


## 1.1.0
### Features
- Added `\()` special value to escape callable key


## 1.0.0
### Features
- Added `load_config_from_file`, `load_config_from_dict`, `load_config_from_yaml_file`,
`load_config_from_json_file` methods
- Added `ConfigLoader` object
