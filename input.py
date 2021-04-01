import make_releases
from constants import ARGUMENTS_DICT, RELEASE_LEVEL_TYPE_DICT
from release_type import ReleaseLevel, ReleaseType


def main():
    import os
    print()
    print("=" * os.get_terminal_size().columns)
    print("Godot Release Script by Sairam".center(os.get_terminal_size().columns, " "))
    print("=" * os.get_terminal_size().columns)
    release_type_raw = input("\tWhat type of release do you want to make?: ")
    release_type = None
    for key in RELEASE_LEVEL_TYPE_DICT:
        if release_type_raw.startswith("c"):
            break
        if key.lower().startswith(release_type_raw.lower()) and ReleaseType.has_value(RELEASE_LEVEL_TYPE_DICT[key]):
            if not release_type:
                release_type = RELEASE_LEVEL_TYPE_DICT[key]
            else:
                print("\tSomething overridden! Exiting!")
                quit(0)

    release_level_raw = input("\tWhich release level do you want your release be set?: ")
    release_level = None
    for key in RELEASE_LEVEL_TYPE_DICT:
        if release_level_raw.startswith("c"):
            break
        if key.lower().startswith(release_level_raw.lower()) and ReleaseLevel.has_value(RELEASE_LEVEL_TYPE_DICT[key]):
            if not release_level:
                release_level = RELEASE_LEVEL_TYPE_DICT[key]
            else:
                print("\tSomething overridden! Exiting!")
                quit(0)
    if not (release_type_raw.startswith("c") and release_level_raw.startswith("c")):
        print(f"\tAre you sure that the information provided is right? Release Type: {release_type}, Release Level: {release_level}: ", end="")
        confirm = input()
        if confirm.lower().startswith("y"):
            make_releases.main(f"{ARGUMENTS_DICT[release_type]} {ARGUMENTS_DICT[release_level]}")

    confirm = input("\tDo you want to clear all releases?: ")
    if confirm.lower().startswith("y"):
        make_releases.main("-clr")

    confirm = input("\tDo you want to release a package with current version?: ")
    if confirm.lower().startswith("y"):
        make_releases.main("-c")


if __name__ == '__main__':  # Main Driver code
    main()
