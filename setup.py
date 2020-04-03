import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arvan",  # Replace with your own username
    version="0.0.5",
    author="silkenpy",
    author_email="silkenpy@gmail.com",
    description="Arvan is python api to work with arvancloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silkenpy/arvan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
