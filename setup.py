import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="firescrape",
    version="0.0.1",
    author="Ayrton Bourn",
    author_email="ayrton@futureenergy.associates",
    description="Fire-Scrape is a Python library for creating scraping projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AyrtonB/Fire-Scrape", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)