## Introduction
This is meant to be a repository of short, general functions or snippets for working with and analyzing chromatographic data.
Functions should be such that they can either be imported and conveniently used, or just copied into a larger workflow.
The power here is that is should be more flexible and adaptable to changes in data or workflow than a fully blown python package.
Functions revolve around simple long form pandas dataframes as in and output.

## Installation
Nothing fancy yet, clone this repository and install whatever packages your system screams at you for not having (rainbow-api being the only non standard one)

## Structure
 - `data_loader.py` Functions for loading data, currently supports just FID and MS data from agilent .D files
 - `analysis.py` Data analysis functions, such as picking and grouping peaks
 - `visualization.py` Various plotting functions


