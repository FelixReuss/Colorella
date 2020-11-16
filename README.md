<img align="right" src="https://github.com/TUW-GEO/colorella/raw/develop/docs/imgs/colorella_logo.png" height="300" width="435">

# Colorella
[![Build Status](https://travis-ci.org/TUW-GEO/colorella.svg?branch=master)](https://travis-ci.org/TUW-GEO/colorella)
[![Coverage Status](https://coveralls.io/repos/github/TUW-GEO/colorella/badge.svg?branch=master)](https://coveralls.io/github/TUW-GEO/colorella?branch=master)
[![PyPi Package](https://badge.fury.io/py/colorella.svg)](http://badge.fury.io/py/colorella)
[![RTD](https://readthedocs.org/projects/colorella/badge/?version=latest)](http://colorella.readthedocs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
*Colorella* stands for **Col**or **or**ganizing and **e**asy to **l**earn **la**boratory
and provides a colormap class that allows the usage of colormaps from different sources and functions for their efficient application. Currently the import from Colormaps from Matplotlib, Colorcet and .cpt, .ct and .json files is supported. Functionality includes showing, reversering, converting colormaps to greyscale, converting and importing to and from Gdal colortables as well as saving colormaps to various formats (.cpt, .ct, .json). For a complete documentation please read the documentation or have a look at the examples in /examples.

## Installation
To install the lastest release of colorella in your own environment, use:

pip install colorella

Installing a specific branch and creating an environment with conda can also be performed using the following commands:

git clone git@github.com:TUW-GEO/colorella.git@branch colorella

cd colorella

conda env create -f environment.yml

source activate colorella

## Citation
If you use the software in a publication then please cite it using the Zenodo DOI.
Be aware that this badge links to the latest package version.

Please select your specific version at xxxxx to get the DOI of that version.
You should normally always use the DOI for the specific version of your record in citations.
This is to ensure that other researchers can access the exact research artefact you used for reproducibility.

You can find additional information regarding DOI versioning at http://help.zenodo.org/#versioning


## Note
This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.

This packages includes colormaps from https://zenodo.org/record/4153113#.X66Mz3XYqV6 described in the following paper: https://www.nature.com/articles/s41467-020-19160-7
