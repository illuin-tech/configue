import os

import setuptools

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="configue",
    version="DEV",
    url="https://github.com/illuin-tech/configue/",

    author="Illuin Technology",
    author_email="contact@illuin.tech",

    description="Helpers to load your application configuration from YAML files",
    long_description=long_description,
    long_description_content_type="text/markdown",

    zip_safe=False,
    platforms="any",

    install_requires=[
        "pyyaml>=5.1.0,<6.0.0",
    ],
    python_requires=">=3.6,<4.0",
    packages=setuptools.find_packages(include=["configue", "configue.*"]),

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
