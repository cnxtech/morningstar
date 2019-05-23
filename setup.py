import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='morningstar',
    version='0.2.2',
    description='Morningstar API Client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aaaccell/morningstar',
    author='Marc Juchli',
    author_email='marcjuchli@aaaccell.ch',
    license='MIT',
    zip_safe=False,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
