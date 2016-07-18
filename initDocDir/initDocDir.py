#!/usr/bin/env python

import argparse
import sys
import os

parser = argparse.ArgumentParser(description= """
DESCRIPTION

Convenience script to initialize a directory tree for project documentation.

USAGE
initDocDir.py mydir

Will create the following tree:

mydir
|-- README.md
|-- mydir.md
|-- data
    `-- README.md
|-- figures
    `-- README.md

Subdirectories are create as necessary, e.g initDocDir.py /path/to/mydir will create
/path/to if necessary.
""", formatter_class= argparse.RawTextHelpFormatter, prog= os.path.basename(__file__))

parser.add_argument('basename',
                   help='''Basename for top directory name and markdown file.
                   ''')

parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')

if __name__ == '__main__':

    args= parser.parse_args()

    basedir= os.path.normpath(args.basename)
    datadir= os.path.join(basedir, 'data')
    figdir= os.path.join(basedir, 'figures')

    dirs= [basedir, datadir, figdir]

    ## Check any of these dirs are files
    for x in dirs:
        if os.path.isfile(x):
            sys.stderr.write('Cannot create dir: %s as this is a file.\n' %(basedir))
            sys.exit(1)
        if os.path.exists(x) and not os.access(x, os.W_OK):
            sys.stderr.write('Dir not writable: %s.\n' %(x))
            sys.exit(1)

    # Create dirs
    for x in dirs:
        try:
            if not os.path.exists(x):
                os.makedirs(x)
        except:
            sys.stderr.write('Cannot create dir: %s.\n' %(x))
            sys.exit(1)

    ## README and markdown
    doc= os.path.join(basedir, os.path.basename(basedir) + '.md')
    topreadme= os.path.join(basedir, 'README.md')    
    datareadme= os.path.join(datadir, 'README.md')
    figreadme= os.path.join(figdir, 'README.md')
    
    for x in [topreadme, doc, figreadme, datareadme]:
        if os.path.exists(x) and not os.path.isfile(x):
            sys.stderr.write('Warning: %s exists but is not a file.\n' %(x))
        if not os.path.exists(x):
            x= open(x, 'a')
            x.close()

sys.exit()