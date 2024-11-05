import os
import setuptools


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements():
    reqs_path = os.path.join(__location__, 'requirements.txt')
    with open(reqs_path, encoding='utf8') as f:
        reqs = [line.strip() for line in f if not line.strip().startswith('#')]

    names = []
    for req in reqs:
        names.append(req)
    return {'install_requires': names}


setuptools.setup(
    name="linguaf",
    version="0.1.2",
    author="Aleksandr Perevalov",
    author_email="perevalovproduction@gmail.com",
    description="Python package for calculating famous measures in computational linguistics",
    long_description=long_description,
    license="MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/Perevalov/LinguaF",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    package_data={"": ["resources/stopwords/*.json"]},
    keywords="language features computational linguistics quantitative text analysis",
    **read_requirements()
)
