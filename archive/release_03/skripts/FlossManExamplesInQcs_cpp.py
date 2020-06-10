# skript zum einfuegen von zeilen in qutecsound.cpp fuer die flossmanual examples (~ zeile 3222)

exampleDir = '/home/jh/src/qutecsound/examples/FLOSS Manual Examples'

print '\n exampleDir = "%s"!' % exampleDir

from os import listdir, walk

def oneChapter(dir):
    """prints out the lines for one chapter. dir is e.g. '/home/jh/src/qutecsound/examples/FLOSS Manual Examples/01 Basics'"""
    lastbsl = dir.rfind("/") #position des letzten slashes
    chap = dir[lastbsl:] #zb /01 Basics
    chapnum = chap[1:3] #sollte 01 ergeben
    files = sorted(listdir(dir))
    print '\n//%s' % chapnum
    for file in files:
        print 'flossman%sFiles.append(":/examples/FLOSS Manual Examples%s/%s");' % (chapnum,chap,file)

    print """	submenu = flossmanMenu->addMenu(tr("%s"));
	foreach (QString fileName, flossman%sFiles) {
		QString name = fileName.mid(fileName.lastIndexOf("/") + 1).replace("_", " ").remove(".csd");
		newAction = submenu->addAction(name);
		newAction->setData(fileName);
		connect(newAction,SIGNAL(triggered()), this, SLOT(openExample()));
	}""" % (chap[1:], chapnum)

subdirs = list(walk(exampleDir))
for dir in sorted(subdirs[0][1]):
    oneChapter('%s/%s' % (exampleDir, dir))


