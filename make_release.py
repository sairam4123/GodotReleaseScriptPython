import argparse
import os
import shutil
import subprocess
import sys

from constants import EXPORT_PATH, EXTENSIONS, FOLDER_NAMES, GODOT, PROJECT_NAME, RELEASES_FOLDER, TYPE
from release_type import ReleaseLevel, ReleaseType
from version_info import VersionInfo, get_version, set_version


def make_release(platform: str, version: VersionInfo):
    if platform not in ['Windows Desktop', 'Mac OSX', 'Linux/X11']:
        raise ValueError(f"can't release for {platform}")

    version_path = EXPORT_PATH / FOLDER_NAMES[version.release_level] / str(version)
    version_path.mkdir(parents=True, exist_ok=True)

    original_path = os.getcwd()
    platform_replaced = platform.replace(' ', '-').replace('/', '-')
    path = (RELEASES_FOLDER / platform_replaced)
    path.mkdir(parents=True, exist_ok=True)

    platform_extraction_folder = f'{PROJECT_NAME}-{platform_replaced}-{version}'

    file_base_name = f"{PROJECT_NAME}-{platform_replaced}-{version}{TYPE[version.release_level]}"

    export_file_name = f'{file_base_name}{EXTENSIONS[platform]}'
    zip_file_name_7z = f'{file_base_name}.7z'

    subprocess.run([GODOT, '--export', f'{platform}', path / export_file_name], shell=True)
    os.chdir(str(path))

    if platform == "Mac OSX":
        subprocess.run(['7z', 'x', export_file_name, '-o' + str(path / platform_extraction_folder)], shell=True)
        (path / export_file_name).unlink()
        os.chdir(str(path / platform_extraction_folder))

    subprocess.run(['7z', 'a', zip_file_name_7z, '.'], shell=True)
    shutil.move(str(path / (platform_extraction_folder if platform == "Mac OSX" else "") / zip_file_name_7z), str(version_path / zip_file_name_7z))
    os.chdir(original_path)
    shutil.rmtree(str(path))


def main():
    version = get_version()

    parser = argparse.ArgumentParser()
    parser.add_argument('--clean-up-releases', '-cl', action='store_true', default=False)
    parser.add_argument('--current', '-c', action="store_true", default=False)
    parser.add_argument('--platform', '-p', action="store")

    release_level_group = parser.add_mutually_exclusive_group()
    release_level_group.add_argument('--alpha', '-a', action="store_const", const=ReleaseLevel.alpha, default=ReleaseLevel.public, dest="release_level")
    release_level_group.add_argument('--beta', '-b', action="store_const", const=ReleaseLevel.beta, default=ReleaseLevel.public, dest="release_level")
    release_level_group.add_argument('--release-candidate', '-rc', action="store_const", const=ReleaseLevel.release_candidate, default=ReleaseLevel.public, dest="release_level")

    release_type_group = parser.add_mutually_exclusive_group()
    release_type_group.add_argument('--major', '-ma', action="store_const", const=ReleaseType.major, dest="release_type")
    release_type_group.add_argument('--minor', '-mi', action="store_const", const=ReleaseType.minor, dest="release_type")
    release_type_group.add_argument('--bugfix', '-bu', action="store_const", const=ReleaseType.bugfix, dest="release_type")
    release_type_group.add_argument('--hotfix', '-ho', action="store_const", const=ReleaseType.hotfix, dest="release_type")

    args = parser.parse_args(sys.argv[1:])

    if not args.current:
        version.increment(args.release_level, args.release_type)
        set_version(version)
    make_release(args.platform, version)


if __name__ == '__main__':  # To test.
    main()
