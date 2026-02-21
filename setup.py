from setuptools import setup, find_packages

setup(
    name="aethercode",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # No external dependencies for now
    ],
    entry_points={
        "console_scripts": [
            "aethercode=aethercode.cli:main",
        ],
    },
)
