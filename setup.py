import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="otdf_python",
    packages=setuptools.find_packages(include=["otdf_python"]),
    py_modules=["otdf_python.gotdf_python"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/b-long/opentdf-python-sdk",
    package_data={"otdf_python": ["*.so"]},
    # Should match 'pyproject.toml' version number
    version="0.0.5",
    include_package_data=True,
)
