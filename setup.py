import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BMJV",
    version="1.0",
    author="Christian Lölkes",
    author_email="christian.loelkes@gmail.com",
    description="Data from the Federal Ministry of Justice and Consumer Protection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hertz-gitlab.zkm.de/rapid-prototyping-lab/python-modules/bmjv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
          'obelixtools'
      ],
)
