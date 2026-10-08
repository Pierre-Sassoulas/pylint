from setuptools import find_namespace_packages, setup

setup(
    name="package1",
    description="package 1",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=["pylint"],
    python_requires=">=3.9",
)
