import setuptools

setuptools.setup(
    name="otdf_python",
    packages=setuptools.find_packages(include=["otdf_python"]),
    py_modules=["otdf_python.gotdf_python"],
    package_data={"otdf_python": ["*.so"]},
    url="https://github.com/b-long/opentdf-python-sdk",
    # Should match 'pyproject.toml' version number
    version="0.0.1",
    include_package_data=True,
)
