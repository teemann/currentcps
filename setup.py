import os
from setuptools import setup, find_packages


def long_description():
    try:
        return open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
    except IOError:
        return None


EXCLUDE_FROM_PACKAGES = [
    'env*',
]

PKG = 'pyplanet_currentcps'
######
setup(
    name=PKG,
    version='1.1.0',
    description='Current CP widget, useful for RPG servers, App for PyPlanet Server Controller',
    long_description=long_description(),
    keywords='maniaplanet, pyplanet, rpg, checkpoint',
    license='GNU General Public License v3 (GPLv3)',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    extras_require={},
    include_package_data=True,
    long_description_content_type='text/markdown',

    author='teemann',
    author_email='teemann100@gmail.com',
    url='https://github.com/teemann/currentcps',

    classifiers=[  # Please update this. Possibilities: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',

        'Operating System :: OS Independent',

        'Topic :: Internet',
        'Topic :: Software Development',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',

    ],
    zip_safe=False, install_requires=['pyplanet']
)
