from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="deepbots",
    author="aidudezzz",
    author_email="deepbots@protonmail.com",
    version="0.0.0.3",
    description=
    "A wrapper framework for Reinforcement Learning in Webots simulator",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_dir={'': 'deepbots'},  # Optional
    packages=find_packages(where='deepbots'),
)
