import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy-equities-client",  # Replace with your username
    version="0.2.3",
    author="delenamalan",
    author_email="<delenamalan@somecompany.com>",
    description="Easy Equity wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/delenamalan/easy-equities-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
