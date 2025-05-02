from setuptools import setup, find_packages

setup(
    name="otdf_python",
    version="0.2.11",
    author="b-long",
    author_email="b-long@users.noreply.github.com",
    description="Buf generated SDK for OpenTDF",
    packages=find_packages("gen"),
    package_dir={"": "gen"},
)
