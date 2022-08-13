# See: https://packaging.python.org/tutorials/packaging-projects/
# for how to install this package on PyPi.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# read version number from package
import e5lora
ver = e5lora.__version__

setuptools.setup(
    name="e5lora",
    version=ver,
    author="Alan Mitchell",
    author_email="tabb99@gmail.com",
    description="Facilitates use of a SEEED Studio E5 LoRaWAN module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alanmitchell/e5lora",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyserial>=3.5',
    ]
)