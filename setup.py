try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    'description': 'db',
    'author': 'Patrick Andruszkiewicz',
    'author_email': 'patrick.andruszkiewicz@uoit.net',
    'version': '0.0.1',
    'packages': find_packages(),
    'name': 'db'
}

setup(**config)
