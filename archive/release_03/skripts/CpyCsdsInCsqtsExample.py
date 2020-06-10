# copies all csd files in the subfolders (starting with the same number or
# name) of the csoundqt examples

from os import listdir, walk, remove
from shutil import copy

srcdir = '/home/jh/Joachim/Csound/FLOSS/Release03/csd_and_audio'
targdir = '/home/jh/src/qutecsound/examples/FLOSS Manual Examples'

# remove all old files
all_folders = walk(targdir)
for folder in all_folders:
    for dat in folder[2]:
        path = '%s/%s' % (folder[0], dat)
        remove(path)

#copy src files in the appropriate folder in targdir
all_src_files = listdir(srcdir)
all_tar_folders = listdir(targdir)
all_tar_folders_numbers = [x[:2] for x in all_tar_folders] #only first two chars of folders
for fil in all_src_files:
    if fil[-4:] == '.csd':
        first_two_chars = fil[:2]
        tar_folder = all_tar_folders_numbers.index(first_two_chars) #index of target folder
        src = '%s/%s' % (srcdir, fil)
        trgt = '%s/%s' % (targdir, all_tar_folders[tar_folder])
        copy(src, trgt)

