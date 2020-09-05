from setuptools import find_packages, setup

DESCRIPTION = "A wrapper framework for Reinforcement Learning in Webots \
    simulator"

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="deepbots",
    author="aidudezzz",
    author_email="deepbots@protonmail.com",
    version="0.1.1",
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
