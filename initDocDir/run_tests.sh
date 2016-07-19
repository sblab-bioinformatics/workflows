#!/bin/bash

echo "Basic usage:"
python initDocDir.py test_data/foo/bar/baz &&
find test_data/foo/bar/baz | sort &&
rm -r test_data/foo/bar/baz
echo ""

echo "Gracefully fail on read only dir:"
chmod 444 test_data/readOnlyDir &&
python initDocDir.py test_data/readOnlyDir &&
chmod 766 test_data/readOnlyDir
