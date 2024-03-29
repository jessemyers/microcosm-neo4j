#!/usr/bin/env python
from setuptools import find_packages, setup

project = "microcosm-neo4j"
version = "0.2.0"

url = "https://github.com/globality-corp/opencypher"

long_description = f"See {url}"
try:
    with open("README.md") as file_:
        long_description = file_.read()
except IOError:
    pass


setup(
    name=project,
    version=version,
    license="Apache 2.0",
    description="OpenCypher AST and Builder API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url=url,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    keywords="opencypher cypher neo4j",
    install_requires=[
        "microcosm>=2.4.1",
        "neo4j>=1.7.1",
        "opencypher>=0.3.0",
    ],
    setup_requires=[
        "nose>=1.3.7",
    ],
    dependency_links=[
    ],
    entry_points={
        "microcosm.factories": [
            "neo4j = microcosm_neo4j.factory:configure_neo4j_driver",
            "neo4j_schema_manager = microcosm_neo4j.schema_manager:SchemaManager",
        ],
    },
    extras_require=dict(
        test="parameterized>=0.6.1",
    ),
    tests_require=[
        "coverage>=4.5.2",
        "parameterized>=0.6.1",
        "PyHamcrest>=1.9.0",
    ],
)
