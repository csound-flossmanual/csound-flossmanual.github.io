# skript zum einfuegen von zeilen in application.qrc fuer die flossmanual examples
# beispiel fuer eine zeile:
# <file>../examples/FLOSS Manual Examples/02 Quick Start/0201.csd</file>

from os import listdir
from os.path import join, isdir, splitext

exampleDir = '/home/jh/src/qutecsound/examples/FLOSS Manual Examples'
print '\n exampleDir = "%s"!' % exampleDir

for dir in sorted(listdir(exampleDir)): #alle ordner, auch verborgene wie .svn
    chap = join(exampleDir,dir) #alle kapitel, auch verborgene, als ganzer pfad
    if isdir(chap): #wenn es ein ordner ist:
        for file in listdir(chap): 
            if splitext(file)[1] == ".csd": #und die endung .csd
                print "        <file>../examples/FLOSS Manual Examples/%s/%s</file>" % (dir,file)
