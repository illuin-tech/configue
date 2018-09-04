# Changelog

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
