from setuptools import setup, find_packages

setup(
    name="graph_ml_converter",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "networkx>=3.1",
        "PyQt6>=6.5.0",
    ],
    entry_points={
        "console_scripts": [
            "graph_ml_converter=main:main",
        ],
    },
    python_requires=">=3.6",
    author="Your Name",
    author_email="your.email@example.com",
    description="A cross-platform desktop application for converting between different graph machine learning file formats.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/graph-ml-converter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 