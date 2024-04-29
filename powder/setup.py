from setuptools import find_packages, setup
__version__ = "1.0"
setup(
    name="powder",
    version=__version__,
    description="Ski Trip Planning Tool",
    author="",
    author_email="",
    url="https://github.com/ManvithaPonnapati/shredthepow",
    license="",
    packages=find_packages(),
    install_requires=[
        "langchain==0.1.16"
    ]
)