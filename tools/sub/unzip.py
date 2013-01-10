#!/usr/bin/env python


import os
import os.path
import sys
import zipfile


def unzip(zip_path, output_dir):
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(output_dir)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s zip_path output_dir' % sys.argv[0]
        sys.exit()

    zip_path = sys.argv[1]
    output_dir = sys.argv[2]
    unzip(zip_path, output_dir)

