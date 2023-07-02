# FutureSight

Repository for Magic the Gathering+Python project to explore and simulate conditional future sight math. Developed in order to optimize the Party Time preconstructed deck, distributed in the expansion Commander Legends: battle for Baldur's Gate.


# Installation

Installation on a conda environment in highly reccommended. To create an appropriate conda environment, use

    conda create fsigh python=3.10
    conda activate fsigh

For more information on coda, see [Conda official page](https://docs.conda.io/en/latest/miniconda.html).

The project has not been published to PyPI yet and local installation is currenlty required.
To install this repository, first clone the current github folder

    git clone https://github.com/Zicchio/FutureSight.git
    cd FutureSight

The library requirements can be installed with pip using the following command (in the folder with this document).

    cd futuresight
    python -m pip install -r requirements.txt

Then you can locally install with

    python -m pip install .


# Usage

The library is shipped with a CLI program that can be called if the library has been installed. To call the program, assuming it has been installe din a Conda environment, use

    python -m futuresight --help

This will display an helper with options. The most common usage is

    python -m futuresight 99 [number of cards in the deck that can be played from top] --htp [number of cards that can be played in a turn form top of library]

# Uninstall

If pip rocedure has been followed for installation, to uninstall use

    python -m pip uninstall futuresight

If you usare using a conda environment, you might need to use `conda clean -ay`.

# TODO

- [ ] Extended documentation
- [ ] Creation of automated plots
- [ ] Support for multityped cards from top (ex: max 1 land from top, max 3 non-lands from top)
- [ ] Support for Party Size simulation tool