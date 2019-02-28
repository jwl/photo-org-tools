import sys
import mac_tag

from os import listdir, remove
from os.path import isfile, join


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
        deletedFiles.append(f)
        remove(filepath + "/" + f)

# Delete un-tagged RAW/ORF files
for f in listdir(filepath + "/raw"):
    if f not in set(rawFiles):
        deletedFiles.append(f)
        remove(filepath + "/raw/" + f)

print(f"Deleted the following files: {deletedFiles}")