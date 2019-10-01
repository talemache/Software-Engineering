from setuptools import setup, find_packages
from setuptools.extension import Extension

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='OOZero',
    description='OOZero reminder application',
    py_modules=['OOZero', 'config'],
    install_requires=requirements,
    zip_safe=False,
    entry_points={
        'console_scripts':[#Define console commands here
        ]
    },
    ext_modules=[ #Incase we want to make c extentions
    ]
)
