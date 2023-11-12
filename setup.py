from setuptools import setup

VERSION = "0.0.1"

setup(
    name="pyavaccess",
    version=VERSION,
    packages=["pyavaccess"],
    description="Automation library for AV Access devices",
    url="https://github.com/latelylk/pyavaccess",
    install_requires=["pyserial>=3.5"],
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
)
