import setuptools

setuptools.setup(
    name="configue",
    version="DEV",
    url="https://github.com/illuin-tech/configue/",

    author="Illuin Technology",
    author_email="contact@illuin.tech",

    description="Helpers to load config files, based on logging.config",

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
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
