from setuptools import setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="python_loki_logger",
    version="3.0.0",
    description="A Python Library for pushing logs to Grafana-Loki",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Piyush Manolkar",
    author_email="manolkarpiyush@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=["python_loki_logger"],
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.8",
)
