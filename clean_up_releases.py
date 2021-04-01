import shutil
from configparser import ConfigParser

from constants import EXPORT_PATH, PROJECT_FOLDER
from version_info import VersionInfo


def clean_up_version() -> None:
    config = ConfigParser()
    with open(str(list(PROJECT_FOLDER.glob("export_presets.cfg"))[0]), 'r') as exports_config:

        config.read_file(exports_config)

        for section_name, section in config.items():
            for key, value in section.items():
                if key.endswith('version'):
                    config.set(section_name, key, VersionInfo.start_version().convert_to_godot_format())

        config_file = open(str(list(PROJECT_FOLDER.glob("export_presets.cfg"))[0]), "w")
        config.write(config_file)
        config_file.close()


def clean_up_releases():
    if input("Do you want to continue? (Yes or No): ").lower().startswith('y'):
        shutil.rmtree(EXPORT_PATH, ignore_errors=True)
        print("Cleaned.")
    else:
        print("Cancelled.")


if __name__ == '__main__':  # Test Script
    clean_up_version()
    clean_up_releases()
