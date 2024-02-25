"""Python setup.py for project_name package"""
from os import path
from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Argume
setup(
    name="microchip_factory",
    version="1.0.0",
    description="Microchip Factory Tools",
    url="",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Edward Nauwelaerts",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "find-responsible-bot=microchip_factory.find_responsible_bot:main",
            "multiply-output-values=microchip_factory.multiply_output_values:main"
        ],
    },
)
