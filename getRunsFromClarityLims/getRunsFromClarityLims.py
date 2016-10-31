#!/usr/bin/env python

import urllib2
import xml.etree.ElementTree as ET
import sys
from collections import Counter

docstring= """
DESCRIPTION
Query clarity lims to collect runs from SBLab

USAGE
getRunsFromClarityLims.py 

See also https://genomicsequencing.cruk.cam.ac.uk/glsintapi/
"""

"""
First collect all the SLX IDs done by SBLab
"""

if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
    print docstring
    sys.exit()

query= 'https://genomicsequencing.cruk.cam.ac.uk/glsintapi/librariesByLab?lab=CRUKCI%20Shankar%20Balasubramanian'

sys.stderr.write('Collecting SLX IDs with:\n%s\n' %(query))

response = urllib2.urlopen(query)
html = response.read()

tree = ET.ElementTree(ET.fromstring(html))

root = tree.getroot()

slxSet= set()
for child in root:
    slx= child.findall('slxId')
    for id in slx:
        slxSet.add(id.text)

sys.stderr.write('Found %s SLX IDs\n' %(len(slxSet)))

"""
Now query runs with the given SLX IDs
"""

## This will construct a query string like 
## https://genomicsequencing.cruk.cam.ac.uk/glsintapi/runsContainingLibraries?slxid=SLX-10672&slxid=SLX-11359&slxid=...

api= 'https://genomicsequencing.cruk.cam.ac.uk/glsintapi/runsContainingLibraries?slxid='
## query= '&slxid='.join(['SLX-6453', 'SLX-5380', 'SLX-9957'])
query= '&slxid='.join(slxSet)

sys.stderr.write('Retrieving information with:\n%s\n' %(api))

response = urllib2.urlopen(api + query)
html = response.read()
tree = ET.ElementTree(ET.fromstring(html))
root = tree.getroot()

## For an exampkle of this XML:
## https://genomicsequencing.cruk.cam.ac.uk/glsintapi/runsContainingLibraries?slxid=SLX-6380

lanes= []
slxFound= set()
for xrun in root:
    flowcells= xrun.findall('flowcell')
    for flowcell in flowcells:
        runType= xrun.find('runType').text
        runFinishDate= xrun.find('finishDate').text
        libraries= flowcell.findall('library') ## 'library' is effectively a lane
        for lib in libraries: 
            slxs= lib.findall('slxId')
            if len(slxs) != 1:
                sys.stderr.write('Found more than one slx for %s\n' %(lib))
                sys.exit(1)
            slxId= slxs[0].text
            if slxId in slxSet: 
                slxFound.add(slxId)
                lanes.append((runType, runFinishDate, slxId))

sys.stderr.write( 'SLXs not found:\n' + [x for x in slxSet if x not in slxFound] )

"""
Report
"""
print '\t'.join(['runType', 'runFinishDate', 'slxId', 'nLanes'])
grpLane= Counter(lanes)
for k in grpLane:
    print '\t'.join(k) + '\t' + str(grpLane[k])