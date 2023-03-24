# Automated detection of _Rana sierrae_ vocalizations

This repository contains scripts related to the analyses and methods of a manuscript submitted to the American Naturalist:

> Lapp, Smith, and Kitzes, _in prep_. "Aquatic soundscape recordings reveal diverse vocalizations and nocturnal activity of an endangered frog".


This notebook uses an open-source dataset of annotated _Rana sierrae_ vocalizations from aquatic soundscape recordings. That dataset is available on Dryad: 
> Lapp, Sam; Kitzes, Justin (2023), Rana sierrae annotated aquatic soundscapes 2022, Dryad, Dataset, https://doi.org/10.5061/dryad.9s4mw6mn3

The repository contains six notebooks which each demonstrate one step of the analyses described in the manuscript:

1. Explore annotated dataset of _Rana sierrae_ call types

2. Prepare annotated files for training a Convolutional Nerual Network  (CNN) machine learning model

3. Train a CNN to recognize _Rana sierrae_ vocaliztaions

4. Analyze the accuracy and performance of the CNN

5. Use the CNN to detect vocalizations in unlabeled data

6. Analyze temporal patterns of vocal activity using the CNN detections


These notebooks use the Python package OpenSoundscape version 0.8.0. Note that the notebooks might not be fully compatible with other versions of OpenSoundscape. 

Questions regarding the analysis, data availability, or adaptation of this code for other purposes can be directed to Sam Lapp (sam.lapp@pitt.edu). 
