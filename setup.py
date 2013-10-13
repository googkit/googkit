import os
from setuptools import setup
import googkit


def data_files(data_dirs):
    result = []

    for data_dir in data_dirs:
        for root, dirnames, filenames in os.walk(data_dir):
            paths = [os.path.join(root, f) for f in filenames]
            result.append((root, paths))

    return result


setup(
    name='googkit',
    version=googkit.VERSION,
    author='cocopon & OrgaChem',
    author_email='cocopon@me.com',
    description='Easier way to develop your web app with Google Closure Library',
    license='MIT',
    keywords='',
    url='https://github.com/cocopon/googkit',
    long_description='TODO: long description',
    packages=[
        'googkit',
        'googkit/cmds',
        'googkit/lib',
        'googkit/plugins'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        "Topic :: Utilities",
    ],
    entry_points={
        'console_scripts': [
            'googkit=googkit:main'
        ]
    },
    zip_safe=False,
    data_files=data_files([
        'config',
        'etc',
        'template'
    ])
)
