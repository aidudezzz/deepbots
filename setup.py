from setuptools import find_packages, setup

DESCRIPTION = "A wrapper framework for Reinforcement Learning in Webots \
    simulator"

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="deepbots",
    author="aidudezzz",
    author_email="deepbots@protonmail.com",
    version="1.0.0",
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
)
