# WSL path converter

Convert between Linux and Windows path in [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) (Windows Subsystem for Linux).

## Installation

Either install the latest stable version hosted on [PyPI](https://pypi.org/):

    pip install wsl-path-converter

Or clone the source repository and install the bleeding-edge version:

    git clone https://github.com/lamyj/wsl-path-converter.git
    cd wsl-path-converter
    pip install .

If the latter case is run by a regular user, i.e. non-root, the `wpc` executable will be installed in `~/.local/bin`.

## Usage

This converter works with Windows path mounted in WSL, either through `/etc/fstab` or through the `mount` command.

The executable is called `wpc`. To convert a Windows path to its Linux counterpart, run it with the `-u` option:

    wpc -u C:\autoexec.bat

This is also valid using [UNC](https://en.wikipedia.org/wiki/Path_(computing)#Uniform_Naming_Convention) paths (e.g. remote shares):
    
    wpc -u \\samba.example.com\share

For the converse operation, i.e. convert a Linux path to its Windows counterpart, use the `-w` option:

    wpc -w /mnt/c/autoexec.bat

If a path unambiguously belongs to either Windows or Linux, the conversion option can be skipped; all previous examples can be run without the option:

    wpc C:\autoexec.bat
    wpc \\samba.example.com\share
    wpc /mnt/c/autoexec.bat
