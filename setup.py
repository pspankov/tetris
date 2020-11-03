import setuptools
import tetris

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tetris",
    version=tetris.__version__,
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
    keywords='python tetris game with turtle graphics',
    entry_points={
        "console_scripts": [
            "tetris = tetris.__main__:main",
        ]
    }
)
