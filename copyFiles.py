# copyFiles handles taking files from the copyFiles folder and copying them to other locations
import shutil, os
from os import listdir
from os.path import isfile, join

def copyAllFiles(directoryToCopyTo):
    files = [f for f in listdir("./copyFiles") if isfile(join("./copyFiles", f))]
    for f in files:
        shutil.copy(os.path.join("./copyFiles",f), os.path.join(directoryToCopyTo,f))