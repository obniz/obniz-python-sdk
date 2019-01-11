import setuptools

from obniz.__version__ import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="obniz",
    version=__version__,
    author="yukisato",
    author_email="yuki@yuki-sato.com",
    description="obniz sdk for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://obniz.io/",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyee==5.0.0',
        'websockets==7.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
    ],
)
