import clean_up_releases
from constants import ARGUMENT_PARSER_CREATOR
from make_release import make_release
from release_type import ReleaseLevel, ReleaseType
from version_info import get_version, set_version


def clean_releases():
    clean_up_releases.clean_up_version()
    clean_up_releases.clean_up_releases()


def make_releases(platforms, release_type: ReleaseType, release_level: ReleaseLevel, current: bool = False):
    version = get_version()

    if not current:
        version.increment(release_level, release_type)
        set_version(version)

    for platform in platforms:
        make_release(platform, version)


def main(parse_args: str):
    import argparse
    import shlex

    parser = ARGUMENT_PARSER_CREATOR()

    args = parser.parse_args(shlex.split(parse_args))

    if args.clean_up_releases:
        clean_releases()
    else:
        platforms = ['Windows Desktop', 'Mac OSX', 'Linux/X11']
        make_releases(platforms, args.release_type, args.release_level, args.current)
        print("\a")


if __name__ == '__main__':  # Test Script
    import sys

    main(" ".join(sys.argv[1:]))
