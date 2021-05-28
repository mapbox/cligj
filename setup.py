from codecs import open as codecs_open

from setuptools import setup, find_packages

with open("cligj/__init__.py") as f:
    for line in f:
        if "__version__" in line:
            version = line.split("=")[1].strip().strip('"').strip("'")
            continue

with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="cligj",
    version=version,
    description=u"Click params for commmand line interfaces to GeoJSON",
    long_description=long_description,
    classifiers=[],
    keywords="",
    author=u"Sean Gillies",
    author_email="sean@mapbox.com",
    url="https://github.com/mapbox/cligj",
    license="BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4",
    install_requires=["click >= 4.0"],
    extras_require={"test": ["pytest-cov"],},
)
