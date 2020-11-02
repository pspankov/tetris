import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-YOUR-USERNAME-HERE",  # Replace with your own username
    version="1.0",
    author="Pavel Pankov",
    author_email="pspankov@gmail.com",
    description="A Tetris game build with turtle graphics package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pspankov/python-tetris",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
