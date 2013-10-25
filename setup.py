import os
from setuptools import setup
import googkit


def read(path):
    script_dir = os.path.dirname(__file__)
    return open(os.path.join(script_dir, path)).read()


def packages(top_dir):
    result = []

    for root, dirnames, filenames in os.walk(top_dir):
        basename = os.path.basename(root)
        if basename == '__pycache__':
            continue

        result.append(root)

    return result


def package_data(package):
    result = []

    for root, dirnames, filenames in os.walk(package):
        comps = root.split(os.sep)[1:]
        path = os.path.join(*comps) if len(comps) > 0 else ''
        result.append(os.path.join(path, '*.*'))

    return {package: result}


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
    long_description=read('README.rst'),
    packages=packages('googkit') + packages('googkit_data'),
    package_data=package_data('googkit_data'),
    classifiers=[
        'Development Status :: 4 - Beta',
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
        'etc',
        'etc/completion'
    ])
)
