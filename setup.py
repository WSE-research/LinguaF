import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LinguaF",
    version="0.0.1",
    author="Aleksandr Perevalov",
    author_email="perevalovproduction@gmail.com",
    description="Python package for calculating famous measures in computational linguistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Perevalov/LinguaF",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)