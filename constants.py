from configparser import ConfigParser, ParsingError
from pathlib import Path

from release_type import ReleaseLevel, ReleaseType


def get_project_name() -> str:
    def add_section_header(config_file, header_name):  # To add section header to the project.godot, without changing anything to the file.
        yield f'[{header_name}]\n'
        for line in config_file:
            yield line

    project_config = list(PROJECT_FOLDER.glob("project.godot"))[0].open('r')

    config = ConfigParser(strict=False)
    try:
        config.read_file(add_section_header(project_config, "defaults"))
    except ParsingError:
        pass
    return config['application']['config/name'].replace('"', "")


RELEASE_LEVEL_DICT = {
    ReleaseLevel.alpha: "a",
    ReleaseLevel.beta: "b",
    ReleaseLevel.release_candidate: "rc",
    ReleaseLevel.public: "",
}

RELEASES_FOLDER = Path.cwd() / 'releases' if 'releases' not in str(Path.cwd()) else Path.cwd()
PROJECT_FOLDER = RELEASES_FOLDER.parent

PROJECT_NAME = get_project_name()
EXPORT_PATH = RELEASES_FOLDER / PROJECT_NAME

GODOT = 'godot'

EXTENSIONS = {
    'Windows Desktop': '.exe',
    'Mac OSX': '.zip',
    'Linux/X11': '.x86_64'
}
TYPE = {
    ReleaseLevel.alpha: "_A",
    ReleaseLevel.beta: "_B",
    ReleaseLevel.release_candidate: "_RC",
    ReleaseLevel.public: ""
}

FOLDER_NAMES = {
    ReleaseLevel.alpha: "Alpha",
    ReleaseLevel.beta: "Beta",
    ReleaseLevel.release_candidate: "Release Candidate",
    ReleaseLevel.public: "Public"
}

RELEASE_LEVEL_TYPE_DICT = {
    "Alpha": ReleaseLevel.alpha,
    "Beta": ReleaseLevel.beta,
    "Release Candidate": ReleaseLevel.release_candidate,
    "Public": ReleaseLevel.public,
    "Major": ReleaseType.major,
    "Minor": ReleaseType.minor,
    "Bugfix": ReleaseType.bugfix,
    "Hotfix": ReleaseType.hotfix,
    "RC": ReleaseLevel.release_candidate,
    "Patch": ReleaseType.bugfix,
}

ARGUMENTS_DICT = {
    ReleaseType.major: "-ma",
    ReleaseType.minor: "-mi",
    ReleaseType.bugfix: "-bu",
    ReleaseType.hotfix: "-ho",
    ReleaseLevel.alpha: "-a",
    ReleaseLevel.beta: "-b",
    ReleaseLevel.release_candidate: "-rc",
    ReleaseLevel.public: "",
}
