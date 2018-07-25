import setuptools

setuptools.setup(
    name="illuin_config",
    version="DEV",
    url="https://gitlab.illuin.tech/bot-factory/illuin-config/",

    author="Illuin Technology",
    author_email="contact@illuin.tech",

    description="Helpers to load config files, based on logging.config",

    zip_safe=False,
    platforms="any",

    install_requires=[
        "pyyaml>=3.13.0,<4.0.0",
    ],
    python_requires=">=3.6,<4.0",
    packages=setuptools.find_packages(include=["illuin_config"]),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
