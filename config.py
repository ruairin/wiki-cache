"""
# @ author: ruairin
# @ about: Reads app configuration from config.yml
# @ usage: import config
#          # read config for search script and connection
#          config_dict = config.read_config('wiki_search_script')
#          # read config for mysql server
#          config_dict = config.read_config('mysql')
"""

import yaml


def read_config(param=None):
    """
    Reads the app configuration from config.yml
    A parameter can be provided to read either the 'mysql' or 'wiki_search_script'
    configuration parameters. If no parameter is provided a dictionary is returned which contains
    the whole configuration

    :param param: String specifying either
    :return: A dictionary containing the configuration parameters, structured according to the config.yml file
    """
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    # if no argument was provided, return the whole configuration file structure
    if not param:
        return config

    # Handle the case where an incorrect param is provided
    # returns the whole config file structure if param is invalid
    try:
        return config[param]
    except KeyError as e:
        print(f'Incorrect parameter {param}')
        return config


if __name__ == '__main__':
    config = read_config()
    print(config.keys())

    config = read_config('postgres')
    print(config)




