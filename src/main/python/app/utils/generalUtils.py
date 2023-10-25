import os

import yaml


# class GeneralUtils:
#     @staticmethod
#     def read_yaml(yaml_path):
#         with open(yaml_path, 'r') as yaml_file:
#             return yaml.safe_load(yaml_file)


class GeneralUtils:
    @staticmethod
    def read_yaml(relative_yaml_path):
        # Identify the path of this script
        current_script_path = os.path.abspath(__file__)

        # Identify the root directory of the project
        # In this case, we navigate up the directory structure 5 times to reach the project root
        project_root_dir = os.path.abspath(os.path.join(os.path.dirname(current_script_path), '..', '..', '..', '..', '..'))

        # Create the absolute path by joining the project root directory with the relative path
        absolute_yaml_path = os.path.join(project_root_dir, relative_yaml_path.lstrip('/'))

        # Open and read the YAML file
        with open(absolute_yaml_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

    @staticmethod
    def resolve_full_path(filename, dir_type):
        current_script_path = os.path.abspath(__file__)
        project_root_dir = os.path.abspath(
            os.path.join(os.path.dirname(current_script_path), '..', '..', '..', '..', '..'))
        data_dir = os.path.join(project_root_dir, 'data', dir_type)
        return os.path.join(data_dir, filename)
