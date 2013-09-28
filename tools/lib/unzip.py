import os
import os.path
import sys
import zipfile


def run(zip_path, output_dir):
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(output_dir)
