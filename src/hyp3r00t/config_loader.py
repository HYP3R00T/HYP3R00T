import yaml


def load_config(path: str) -> dict:
    """
    Load and return configuration from a YAML file.
    """
    with open(path) as file:
        config = yaml.safe_load(file)

    return config
