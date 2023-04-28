from setuptools import setup, find_packages

setup(
    name="bifrost-cFS",
    version="0.0.0",
    url="https://github.com/Mejiro-McQueen/Bifrost-NASA-cFS",
    author="Mejro-McQueen",
    author_email="",
    description='Bifrost Expansion for the NASA Core Flight Software',
    python_requires='>=3.8',
    install_requires=[
    ],
    packages=find_packages(),
    scripts= [ ],
    extras_require={
        'tests': [
            "pytest",
        ],
    },
)
