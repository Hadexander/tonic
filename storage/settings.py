import configparser

config_file = 'config.ini'

def load(section:str):
    """Returns a config section with the given name as a dictionary."""
    config = configparser.ConfigParser()
    with open(config_file, 'r') as f:
        config.read_file(f)
    return config[section]

def save(section:str, contents:dict):
    """Saves a config section."""
    config = configparser.ConfigParser()
    config[section] = contents
    with open(config_file, 'w') as f:
        config.write(f)