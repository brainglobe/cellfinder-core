[![Python Version](https://img.shields.io/pypi/pyversions/cellfinder-core.svg)](https://pypi.org/project/cellfinder-core)
[![PyPI](https://img.shields.io/pypi/v/cellfinder-core.svg)](https://pypi.org/project/cellfinder-core)
[![Downloads](https://pepy.tech/badge/cellfinder-core)](https://pepy.tech/project/cellfinder-core)
[![Wheel](https://img.shields.io/pypi/wheel/cellfinder-core.svg)](https://pypi.org/project/cellfinder-core)
[![Development Status](https://img.shields.io/pypi/status/cellfinder-core.svg)](https://github.com/brainglobe/cellfinder-core)
[![Tests](https://img.shields.io/github/workflow/status/brainglobe/cellfinder-core/tests)](
    https://github.com/brainglobe/cellfinder-core/actions)
[![Coverage Status](https://coveralls.io/repos/github/brainglobe/cellfinder-core/badge.svg?branch=main)](https://coveralls.io/github/brainglobe/cellfinder-core?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Gitter](https://badges.gitter.im/brainglobe.svg)](https://gitter.im/BrainGlobe/cellfinder/?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://docs.brainglobe.info/cellfinder/contributing)
[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fcellfinder.info)](https://cellfinder.info)
[![Twitter](https://img.shields.io/twitter/follow/findingcells?style=social)](https://twitter.com/findingcells)
# cellfinder-core
Standalone cellfinder cell detection algorithm 

This package implements the cell detection algorithm from 
[Tyson, Rousseau & Niedworok et al. (2021)](https://www.biorxiv.org/content/10.1101/2020.10.21.348771v2) 
without any dependency on data type (i.e. it can be used outside of 
whole-brain microscopy). 

`cellfinder-core` supports the 
[cellfinder](https://github.com/brainglobe/cellfinder) software for 
whole-brain microscopy analysis, and the algorithm can also be implemented in 
[napari](https://napari.org/index.html) using the 
[cellfinder napari plugin](https://github.com/brainglobe/cellfinder-napari).

---

## Instructions

### Installation
`cellfinder-core` supports Python 3.7, 3.8 (3.9 when supported by TensorFlow), 
and works across Linux, Windows, and should work on most versions of macOS 
(although this is not tested).

Assuming you have a Python 3.7 or 3.8 environment set up 
(e.g. [using conda](https://docs.brainglobe.info/cellfinder/using-conda)), 
you can install `cellfinder-core` with:
```bash
pip install cellfinder-core
```

Once you have [installed napari](https://napari.org/index.html#installation). 
You can install napari either through the napari plugin installation tool, or 
directly from PyPI with:
```bash
pip install cellfinder-napari
```

N.B. To speed up cellfinder, you need CUDA & cuDNN installed. Instructions 
[here](https://docs.brainglobe.info/cellfinder/installation/using-gpu).

### Usage
Before using cellfinder-core, it may be useful to take a look at the 
[preprint](https://www.biorxiv.org/content/10.1101/2020.10.21.348771v2) which
outlines the algorithm.

---
### More info

More documentation about cellfinder and other BrainGlobe tools can be 
found [here](https://docs.brainglobe.info). 
 
This software is at a very early stage, and was written with our data in mind. 
Over time we hope to support other data types/formats. If you have any 
questions or issues, please get in touch by 
[email](mailto:code@adamltyson.com?subject=cellfinder-core), 
[gitter](https://gitter.im/BrainGlobe/cellfinder) or by 
[raising an issue](https://github.com/brainglobe/cellfinder-core/issues).

---
## Illustration

### Introduction
cellfinder takes a stitched, but otherwise raw whole-brain dataset with at least 
two channels:
 * Background channel (i.e. autofluorescence)
 * Signal channel, the one with the cells to be detected:
 
![raw](https://raw.githubusercontent.com/brainglobe/cellfinder/master/resources/raw.png)
**Raw coronal serial two-photon mouse brain image showing labelled cells**


### Cell candidate detection
Classical image analysis (e.g. filters, thresholding) is used to find 
cell-like objects (with false positives):

![raw](https://raw.githubusercontent.com/brainglobe/cellfinder/master/resources/detect.png)
**Candidate cells (including many artefacts)**


### Cell candidate classification
A deep-learning network (ResNet) is used to classify cell candidates as true 
cells or artefacts:

![raw](https://raw.githubusercontent.com/brainglobe/cellfinder/master/resources/classify.png)
**Cassified cell candidates. Yellow - cells, Blue - artefacts**

---
## Citing cellfinder
If you find this plugin useful, and use it in your research, please cite the preprint outlining the cell detection algorithm:
> Tyson, A. L., Rousseau, C. V., Niedworok, C. J., Keshavarzi, S., Tsitoura, C., Cossell, L., Strom, M. and Margrie, T. W. (2021) “A deep learning algorithm for 3D cell detection in whole mouse brain image datasets’ bioRxiv, [doi.org/10.1101/2020.10.21.348771](https://doi.org/10.1101/2020.10.21.348771)


**If you use this, or any other tools in the brainglobe suite, please
 [let us know](mailto:code@adamltyson.com?subject=cellfinder-core), and 
 we'd be happy to promote your paper/talk etc.**
