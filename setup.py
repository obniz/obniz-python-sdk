import setuptools
from codecs import open
from os import path
import re

package_name = "obniz"
root_dir = path.abspath(path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(path.join(root_dir, package_name, '__init__.py')) as f:
    init_text = f.read()
    # license = re.search(r'__license__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author = re.search(r'__author__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author_email = re.search(r'__author_email__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    url = re.search(r'__url__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

with open(path.join(root_dir, package_name, package_name, '__version__.py')) as f:
    init_text = f.read()
    version = re.search(r'__version__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

setuptools.setup(
    name=package_name,
    version=version,
    author=author,
    author_email=author_email,
    description="obniz sdk for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'pyee==6.0.0',
        'websockets==7.0',
        'attrdict==2.0.1',
        'semver==2.8.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
    ],
)
