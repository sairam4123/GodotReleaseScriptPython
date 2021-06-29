import os
import shutil
import subprocess
import sys

from constants import ARGUMENT_PARSER_CREATOR, EXPORT_PATH, EXTENSIONS, FOLDER_NAMES, GODOT, PROJECT_NAME_REPLACED_WITH_HYPENS, RELEASES_FOLDER, TYPE
from version_info import VersionInfo, get_version, set_version


def make_release(platform: str, version: VersionInfo):
    if platform not in ['Windows Desktop', 'Mac OSX', 'Linux/X11', 'HTML5']:
        raise ValueError(f"can't release for {platform}")

    version_path = EXPORT_PATH / FOLDER_NAMES[version.release_level] / str(version)
    version_path.mkdir(parents=True, exist_ok=True)

    original_path = os.getcwd()
    platform_replaced = platform.replace(' ', '-').replace('/', '-')
    path = (RELEASES_FOLDER / platform_replaced)
    path.mkdir(parents=True, exist_ok=True)

    file_base_name = f"{PROJECT_NAME_REPLACED_WITH_HYPENS}-{platform_replaced}-{version}{TYPE[version.release_level]}"

    export_file_name = f'{file_base_name}{EXTENSIONS[platform]}'
    zip_file_name_7z = f'{file_base_name}.7z'

    subprocess.run([GODOT, '--export', f'{platform}', path / export_file_name], shell=True)
    os.chdir(str(path))

    subprocess.run(['7z', 'a', zip_file_name_7z, '.'], shell=True)
    shutil.move(str(path / zip_file_name_7z), str(version_path / zip_file_name_7z))
    os.chdir(original_path)
    shutil.rmtree(str(path))


def main():
    version = get_version()

    parser = ARGUMENT_PARSER_CREATOR()

    args = parser.parse_args(sys.argv[1:])

    if not args.current:
        version.increment(args.release_level, args.release_type)
        set_version(version)
    make_release(args.platform, version)
    print("\a")


if __name__ == '__main__':  # To test.
    main()
