# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
    ['pyvttt',
     'pyvttt.models',
     'pyvttt.shared',
     'pyvttt.shared.exceptions',
     'pyvttt.shared.utils']

package_data = \
    {'': ['*']}

install_requires = \
    ['pydantic>=2.4.2,<3.0.0']

entry_points = \
    {'console_scripts': ['pyvttt = pyvttt:main', 'test = pytest:main']}

setup_kwargs = {
    'name': 'pyvttt',
    'version': '0.1.0',
    'description': 'Python Video-to-Text Transcriber',
    'long_description': '# pyvttt\n\n`pyvttt` is a simple Video-to-Text Transcriber written in Python.\n\n## Installation\n\nThis tool uses [poetry](https://python-poetry.org/) to manage dependencies and packaging. To install all the\ndependencies simply run:\n\n``` shell\npoetry install\n```\n\n## Usage\n\nYou can run the tool using poetry:\n\n``` shell\npoetry run pyvttt --help\n```\n\nOr you can run the tool using python:\n\n``` shell\npython -m pyvttt --help\n```\n\nOr you can run the tool directly from the directory or add it to your path:\n\n``` shell\npyvttt --help\n```\n\n```shell\nusage: pyvttt [-h] [--verbose] [--debug] [--quiet | --no-quiet | -q] [--version]\n\nThis is a template repository to build Python CLI tool.\n\noptions:\n  -h, --help            show this help message and exit\n  --verbose, -v         Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).\n  --debug               Enable debug mode.\n  --quiet, --no-quiet, -q\n                        Do not print any output/log\n  --version             Show version and exit.\n\n```\n\n## Development\n\n### Testing\n\nTo run the tests simply run:\n\n``` shell\npoetry run test\n```\n\n### Update `setup.py`\n\nTo update the `setup.py` file with the latest dependencies and versions run:\n\n``` shell\npoetry run poetry2setup > setup.py\n```\n\n### Acknowledgements\n\nThis project was generated using powerful tools and libraries such as [poetry](https://python-poetry.org/),\n[pydantic](https://docs.pydantic.dev/latest/), [pytest](https://docs.pytest.org/en/stable/) and more, I simply put the\npieces together. Please check and support all the tools and libraries used in this project.',
    'author': 'ZappaBoy',
    'author_email': 'federico.zappone@justanother.cloud',
    'maintainer': 'ZappaBoy',
    'maintainer_email': 'federico.zappone@justanother.cloud',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<3.12',
}

setup(**setup_kwargs)

