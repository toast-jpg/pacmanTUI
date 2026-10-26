from setuptools import setup, find_packages

setup(
    name="pacmantui",
    version="0.1.0",
    py_modules=["main"],
    install_requires=[
        "textual",
    ],
    entry_points={
        "console_scripts": [
            "pacmantui=main:main",
        ],
    },
    author="Toast-jpg",
    description="A simple TUI package manager for Arch Linux using Textual, completely written in python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
)
