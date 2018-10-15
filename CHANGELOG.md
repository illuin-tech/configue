# Changelog
## Unreleased


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
