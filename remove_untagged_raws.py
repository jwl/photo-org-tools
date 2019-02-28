"""Removes any un-tagged JPG and RAW files.

This script takes in a filepath and searches for all JPG photos with the 
"Keep.Photo" tag and deletes JPGs without the tag and all RAW files that do not
have a matching JPG file with a "Keep.Photo" tag. This assumes that all RAW
files are in a "/raw/" subdirectory in the given filepath.
"""
import sys
import mac_tag

from os import listdir, remove
from os.path import isfile, join


def query_yes_no(question: str, default: str ="no") -> bool:
    """
    Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.

    Args:
        question: Question to ask the user as a string.
        default: The answer to default to if user just hits <Enter>.

    Returns:
        Yes as true or No as false

    """
    valid = {"yes": True, "y": True, "ye": True,
            "no": False, "n": False}
    if default is None:
        prompt = " [y/N] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

filepath = sys.argv[1]

jpgFiles = [
    f
    for f in listdir(filepath)
    if isfile(join(filepath, f))
    and mac_tag.get(join(filepath, f))[join(filepath, f)] == ["Keep.Photo"]
]

rawFiles = [
    f[:-3] + "ORF"
    for f in jpgFiles
]

deletedFiles = []

# Delete un-tagged jpg files
for f in listdir(filepath):
    if ".JPG" in f and f not in set(jpgFiles):
        deletedFiles.append(filepath + "/" + f)

# Delete un-tagged RAW/ORF files
for f in listdir(filepath + "/raw"):
    if f not in set(rawFiles):
        deletedFiles.append(filepath + "/raw/" + f)

print("About to delete the following files:")
for f in deletedFiles:
    print(f)
if query_yes_no("Confirm?", "no"):
    for f in deletedFiles:
        remove(f)
    print(f"Deleted the following files: {deletedFiles}")
else:
    print("Aborting file deletion! No files have been deleted.")
