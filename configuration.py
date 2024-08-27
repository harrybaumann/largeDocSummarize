import json

def load_config(config_key: str) -> str:
    """
    Loads a configuration value from the config.json file.

    Args:
        config_key (str): The key of the configuration value to load.

    Returns:
        The configuration value associated with the given key, or None if the key is not found or the config file is invalid.
    """
    config_file_path = "config.json"
    try:
        with open(config_file_path, 'r') as f:
            config = json.load(f)
            config_value = config[config_key]
            if config_value is None:
                print(f"Failed to load config key '{config_key}'. Exiting.")
                return None
            return config_value
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON in config file.")
        return None
