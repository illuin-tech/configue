# Changelog
## Unreleased
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
