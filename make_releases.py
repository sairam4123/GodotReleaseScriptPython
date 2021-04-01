import clean_up_releases
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean-up-releases', '-clr', action='store_true', default=False)
    parser.add_argument('--current', '-c', action="store_true", default=False)

    release_level_group = parser.add_mutually_exclusive_group()
    release_level_group.add_argument('--alpha', '-a', action="store_const", const=ReleaseLevel.alpha, default=ReleaseLevel.public, dest="release_level")
    release_level_group.add_argument('--beta', '-b', action="store_const", const=ReleaseLevel.beta, default=ReleaseLevel.public, dest="release_level")
    release_level_group.add_argument('--release-candidate', '-rc', action="store_const", const=ReleaseLevel.release_candidate, default=ReleaseLevel.public, dest="release_level")

    release_type_group = parser.add_mutually_exclusive_group()
    release_type_group.add_argument('--major', '-ma', action="store_const", const=ReleaseType.major, dest="release_type")
    release_type_group.add_argument('--minor', '-mi', action="store_const", const=ReleaseType.minor, dest="release_type")
    release_type_group.add_argument('--bugfix', '-bu', action="store_const", const=ReleaseType.bugfix, dest="release_type")
    release_type_group.add_argument('--hotfix', '-ho', action="store_const", const=ReleaseType.hotfix, dest="release_type")

    args = parser.parse_args(shlex.split(parse_args))

    if args.clean_up_releases:
        clean_releases()
    else:
        platforms = ['Windows Desktop', 'Mac OSX', 'Linux/X11']
        make_releases(platforms, args.release_type, args.release_level, args.current)


if __name__ == '__main__':  # Test Script
    import sys

    main(" ".join(sys.argv[1:]))
