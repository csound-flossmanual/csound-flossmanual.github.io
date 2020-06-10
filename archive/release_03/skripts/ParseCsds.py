## run this directly before releasing
## parses the html files in cs_floss_url
## and generates all the csd files from the examples

## todo: modify the test-csd script so that long csds
# (for instance f 0 86400) will be terminated after 10 seconds

cs_floss_url = 'http://booki.flossmanuals.net/csound/_draft/_v/1.0/'
csdOutDir = '/home/jh/Joachim/Csound/FLOSS/Release03/csd_and_audio'

print '\n***********************************************'
print 'URL to fetch csd example files is %s' % cs_floss_url
print 'Directory to write csd files to is %s.' % csdOutDir
print '(Note that this dir must already exist.)'
print '***********************************************'

decision = raw_input('Continue? (y/n): ')

if decision == 'n':
    exit()

from sgmllib import SGMLParser

class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []

	def start_a(self, attrs):
		href = [v for k, v in attrs if k=='href']
		if href:
			self.urls.extend(href)

import urllib


def findExample(html, start=0):
    section = html[start:]
    example = section.find('EXAMPLE')
    cssynth_start = section[example:].find('&lt;CsoundSynthesizer&gt;')
    cssynth_end = section[example:].find('&lt;/CsoundSynthesizer&gt;')
    if example != -1 and cssynth_start != -1 and cssynth_end != -1:
        return (example+start, cssynth_start+example+start, cssynth_end+example+start+len('&lt;/CsoundSynthesizer&gt;'))
    else: return -1

def findExamplePositions(html, start=0, erg=[]):
    """returns lists like [(1587, 1648, 2010), (5114, 5180, 5689)].
    first number is the start of the word EXAMPLE, second number is start of the 
    <CsoundSynthesizer> tag, third number is end of the </CsoundSynthesizer> tag."""
    if findExample(html, start) != -1:
        erg.append(findExample(html, start))
        findExamplePositions(html, findExample(html, start)[2], erg)
    return erg

def outfilName(html, examplePos, csSynthPos):
    """schema must be 'EXAMPLE bla.csd'"""
    title = html[examplePos:csSynthPos]
    title = title.split()[1] #csd name ohne spaces
    return title[:title.index('.csd')+4]

def bisFormatted(html, csSynthEnde):
    """returns position of next </pre> tag
    (ensures not to cut authors after example code)"""
    return html.index('</pre>', csSynthEnde)

def tagPlease(string):
    return string.replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ').replace('&amp;', '&')

def examplesToFiles(htmlString, fileDir):
    """gets from a html page of the csound floss manual the csd-code-examples
    and saves as own files in folder fileDir"""
    for example in findExamplePositions(htmlString, 0, []):
        filnam = '%s/%s' % (fileDir, outfilName(htmlString, example[0], example[1]))
        print '  -> Writing %s' % filnam
        outfil = open(filnam, 'w')
        outfil.write(tagPlease(htmlString[example[1]:bisFormatted(htmlString, example[2])]))
        outfil.close()




## get all html pages. they are sub to http://booki.flossmanuals.net/csound/_draft/_v/1.0/

print '\n***********************************************'
print 'Fetching files from %s' % cs_floss_url
print '***********************************************'

cs_sub_url = cs_floss_url[cs_floss_url.index('csound'):]
booki_url = cs_floss_url[:cs_floss_url.index(cs_sub_url)]
all_urls = []
usock = urllib.urlopen(cs_floss_url)
parser = URLLister()
parser.feed(usock.read())
parser.close()
usock.close()
for url in parser.urls: 
    if cs_sub_url in url:
        all_urls.append('%s%s' % (booki_url, url[1:]))


## parse each of the html page and save the csd examples in the folder

for fil in all_urls:
    print 'Analyzing %s' % fil
    f = urllib.urlopen(fil)
    htmlStr = f.read()
    f.close()
    examplesToFiles(htmlStr, csdOutDir)
    

## test all csd files 

from sys import argv
from os import system, chdir, listdir
from os.path import dirname

print '\n***********************************************'
print 'Testing now all .csd files in %s.' % csdOutDir
print '***********************************************'

def isCsd(string):
    if string.rstrip()[-4:] == '.csd':
        return 1
    else:
        return 0

chdir(csdOutDir) 
testSum = 0

for csdfil in sorted(listdir(csdOutDir)):
    if isCsd(csdfil):
        csd = '%s/%s' % (csdOutDir, csdfil)
        print "*Testing file %s ..." % csdfil
        if system('csound -d -+ignore_csopts=1 -n %s 2> /dev/null' % csd) == 0: 
            print "... ok"
        else:
            print "\n********\n... ERROR!!!\n********\n"
            print "*This is Csound's output message:"
            system('csound -d  -+ignore_csopts=1 -n %s' % csd)
            testSum = testSum + 1

print '\n***********************************************'
print 'In total, %d errors while testing' % testSum
print '***********************************************'
