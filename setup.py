# coding=utf-8
from setuptools import setup, find_packages
import io
import re

with io.open("ploto_gidat/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='ploto-gidat',

    version=version,

    description='Ploto-gidat project.',
    long_description=__doc__,

    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

    include_package_data=True,

    package_data={
        '': ['*.ncl'],
    },

    zip_safe=False,

    install_requires=[
        'click',
        'pyyaml',
        'pika',
        'requests',
        'sqlalchemy',
        'loguru',
        "flask",
        "pandas",
    ],

    extras_require={
        'test': [],
        "legacy": [
            'cx_Oracle',
        ]
    }
)