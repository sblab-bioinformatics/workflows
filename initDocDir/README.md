Create directory structure for document repository
==================================================

Simple script to create directories and subdirectories for documenting projects.
Within directories `data` and `figures` put also a README.md. In the top put 
README.md and an .md file with the same name as the top dir itself.

```
./initDocDir.py abc
```

Will create:

```
abc/
├── abc.md
├── data
│   └── README.md
├── figures
│   └── README.md
└── README.md
```

Root directories are created as necessary, e.g. `initDocDir.py foo/bar/abc` will
create `foo/bar` if they don't exists. Existing files and directories are NOT
overwritten.

Typical usage
=============

You start a new piece of work within a project and you want to have a dedicated 
directory and documentation for this. Documentation goes in `abc.md`, figures and 
data in the respective directories. README files can stay empty. Once happy 
you might want to add the all thing to github and commit.

Installation
============

```
wget https://raw.githubusercontent.com/sblab-bioinformatics/workflows/master/initDocDir/initDocDir.py
chmod a+x initDocDir.py
mv initDocDir.py /dir/on/path/ # Optional e.g. /usr/local/bin/ or ~/bin/

initDocDir.py -h 
```