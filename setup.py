import glob
import os

from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="wsl-path-converter",
    version="0.3.1",
    
    description="Convert between Linux and Windows path in WSL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    url="https://github.com/lamyj/wsl-path-converter",
    
    author="Julien Lamy",
    author_email="lamy@unistra.fr",
    
    license="MIT",
    
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        
        "Environment :: Console",
        
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        
        "Topic :: Communications :: File Sharing",
        "Topic :: System :: Archiving :: Mirroring",
        
        "License :: OSI Approved :: MIT License",
        
        "Operating System :: Microsoft :: Windows",
        
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        
        "Topic :: System :: Filesystems",
    ],
    
    keywords="wsl, windows, linux, path",

    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    
    entry_points={ "console_scripts": [ "wpc=wsl_path_converter.main:main"] },
)
