import setuptools


from pathlib import Path

"""
NOTE: This project uses more than one version of a 'setup.py' file:
* 'setup.py', and
* 'setup_ci.py'

Based on:
    https://github.com/popatam/gopy_build_wheel_example/blob/main/setup_ci.py
"""

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="otdf_python",
    packages=setuptools.find_packages(include=["otdf_python"]),
    py_modules=["otdf_python.gotdf_python"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/b-long/opentdf-python-sdk",
    package_data={"otdf_python": ["*.so"]},
    # Should match 'pyproject.toml' version number
    version="0.2.7",
    author_email="b-long@users.noreply.github.com",
    include_package_data=True,
)
