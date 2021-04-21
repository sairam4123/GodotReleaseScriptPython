import re
from configparser import ConfigParser

from constants import PROJECT_FOLDER, RELEASE_LEVEL_DICT
from release_type import ReleaseLevel, ReleaseType, value_from_key


class VersionInfo:
    def __init__(
            self,
            major: int = 0,
            minor: int = 0,
            bugfix: int = 0,
            hotfix: int = 0,
            release_level: ReleaseLevel = ReleaseLevel.public,
            serial: int = None,
            release_type: ReleaseType = None,
            short_version: bool = False,
    ):
        self.major = 0 if major is None else int(major)
        self.minor = 0 if minor is None else int(minor)
        self.bugfix = 0 if bugfix is None else int(bugfix)
        self.hotfix = 0 if hotfix is None else int(hotfix)
        self.short_version = short_version
        self.release_type = release_type

        if self.release_type is None:
            if self.hotfix == 0:
                if self.bugfix == 0:
                    if self.minor == 0:
                        if self.major != 0:
                            self.release_type = ReleaseType.major
                    else:
                        self.release_type = ReleaseType.minor
                else:
                    self.release_type = ReleaseType.bugfix
            else:
                self.release_type = ReleaseType.hotfix

        self.serial = (serial and int(serial)) or 0
        self.release_level = value_from_key(RELEASE_LEVEL_DICT, release_level) or release_level or ReleaseLevel.public

    def __str__(self):
        version: str = f'v{self.major}.{self.minor}.{self.bugfix}'
        if self.release_type == ReleaseType.hotfix:
            version = f'{version}.{self.hotfix}'
        elif self.release_level != ReleaseLevel.public:
            version = f'{version}{RELEASE_LEVEL_DICT[self.release_level]}{self.serial}'
        return version

    def increment(self, release_level: ReleaseLevel, release_type: ReleaseType = None):
        sequel: bool = False
        if release_type == self.release_type and self.release_level == ReleaseLevel.public:
            sequel = True
        if self.release_type != release_type or sequel:

            if release_type == ReleaseType.hotfix:
                self.hotfix += 1
            else:
                self.hotfix = 0
            if release_type == ReleaseType.bugfix:
                self.bugfix += 1
            else:
                self.bugfix = 0
            if release_type == ReleaseType.minor:
                self.minor += 1
            else:
                self.minor = 0
            if release_type == ReleaseType.major:
                self.major += 1

            self.serial = None
            self.release_type = release_type

        if release_level != ReleaseLevel.public:
            self.increase_serial(release_level)

        elif release_level == ReleaseLevel.public:
            self.serial = 0
            self.release_level = release_level
            self.release_type = release_type

    def increase_serial(self, release_level: ReleaseLevel):
        if self.serial is not None and self.release_level != release_level:
            self.serial = 0
        else:
            if self.serial is not None:
                self.serial += 1
            else:
                self.serial = 0
        self.release_level = release_level

    def convert_to_godot_format(self):
        print(str(self))
        return repr(str(self).lstrip("v")).replace("'", '"')

    @classmethod
    def start_version(cls):
        return cls(0, 1, 0)

    @classmethod
    def load_version(cls, version: str):
        pattern: re.Pattern = re.compile(r"(\d)\.(\d)\.?(\d)?\.?(\d)?\.?([a-z]{1,2})?(\d{1,3})?")
        match: re.Match = pattern.match(version.replace('"', ''))
        if match:
            return cls(*match.groups())
        else:
            return cls.start_version()


def set_version(new_version: VersionInfo) -> None:
    config = ConfigParser()
    with open(list(PROJECT_FOLDER.glob("export_presets.cfg"))[0], 'r') as exports_config:

        config.read_file(exports_config)

        for section_name, section in config.items():
            for key, value in section.items():
                if key.endswith('version'):
                    config.set(section_name, key, new_version.convert_to_godot_format())

        config_file = open(list(PROJECT_FOLDER.glob("export_presets.cfg"))[0], "w")
        config.write(config_file)
        config_file.close()


def get_version() -> VersionInfo:
    config = ConfigParser()
    with open(list(PROJECT_FOLDER.glob("export_presets.cfg"))[0], 'r') as exports_config:
        config.read_file(exports_config)

        version: VersionInfo = VersionInfo.start_version()
        for section_name, section in config.items():
            for key, value in section.items():
                if key.endswith('version'):
                    version = VersionInfo.load_version(value)
        return version


if __name__ == '__main__':  # Test Script
    index = 0
    version_info = VersionInfo(1, 0, 0, 0, ReleaseLevel.public, None, ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.alpha, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.alpha, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.public, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.public, release_type=ReleaseType.bugfix)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.public, release_type=ReleaseType.bugfix)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.public, release_type=ReleaseType.hotfix)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.alpha, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.public, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.alpha, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.alpha, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.alpha, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.alpha, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.beta, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.release_candidate, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.public, release_type=ReleaseType.major)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.public, release_type=ReleaseType.hotfix)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.public, release_type=ReleaseType.hotfix)
    print(index, version_info)
    index += 1
    version_info.increment(ReleaseLevel.alpha, release_type=ReleaseType.minor)
    print(index, version_info)
    index += 1

    _version = version_info.convert_to_godot_format()
    print(_version)

    _pattern: re.Pattern = re.compile(r"(\d)\.(\d)\.?(\d)?\.?(\d)?\.?([a-z]{1,2})?(\d{1,3})?")
    _match: re.Match = _pattern.match(_version.replace('"', ''))
    print(index, VersionInfo(*_match.groups()))
