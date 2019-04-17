from setuptools import setup

setup(
    name='pyshellitems',
    version="0.0.1",
    description='Library to handle shellitems.',
    author='Matthew Seyer',
    url='https://github.com/forensicmatt/pyshellitems',
    license='Apache License (2.0)',
    package_dir = {
        '': 'pyshellitems',
        'extensionblocks': 'pyshellitems.extensionblocks',
        'propertystore': 'pyshellitems.propertystore',
        'shellitems': 'pyshellitems.shellitems'
    },
    scripts=[
        'scripts/extract_shellbags.py',
        'scripts/extract_shellitems_from_lnk.py',
        'scripts/parse_shellitems.py'
    ]
)