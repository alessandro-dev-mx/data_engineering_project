import yaml


def open_yaml(filename: str) -> dict:
    """Creates a dictionary out of a YAML file

    :param filename: Path (relative/absolute) of the YAML file to load as a dict
    :type filename: str
    :return: Dictionary containing the key-values from the YAML file
    :rtype: dict
    """    

    with open(filename) as file_obj:
        file_data_dict = yaml.safe_load(file_obj)

    return file_data_dict
