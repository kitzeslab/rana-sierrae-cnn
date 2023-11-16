# Automated detection of _Rana sierrae_ vocalizations

This repository contains scripts related to the analyses and methods of a manuscript accepted for publication in The American Naturalist:

> Lapp, S., Smith, T. C., Wilhelm, A, Knapp, R., Kitzes, J. _In press_. Aquatic soundscape recordings reveal diverse vocalizations and nocturnal activity of an endangered frog. The American Naturalist.

Manuscript Abstract:
> Autonomous sensors provide opportunities to observe organisms across spatial and temporal scales that are not possible with direct human observation. By processing large data streams from autonomous sensors with deep learning methods, researchers can make novel and important natural history discoveries. In this study, we combine automated acoustic monitoring with deep learning models to observe breeding-associated activity in the endangered Sierra Nevada yellow-legged frog (Rana sierrae), behavior that current surveys do not measure. By deploying inexpensive hydrophones and developing a deep learning model to recognize breeding-associated vocalizations, we discover three undocumented R. sierrae vocalization types and find an unexpected temporal pattern of nocturnal breeding-associated vocal activity. This study exemplifies how the combination of autonomous sensor data and deep learning can shed new light on species’ natural history, especially during times or in locations where human observation is limited or impossible.

This repository uses an open-source dataset of annotated _Rana sierrae_ vocalizations from aquatic soundscape recordings. That dataset is available on Dryad: 

> Lapp, Sam; Kitzes, Justin (2023), Rana sierrae annotated aquatic soundscapes 2022, Dryad, Dataset, https://doi.org/10.5061/dryad.9s4mw6mn3

The repository contains six notebooks and one script which each demonstrate one step of the analyses described in the manuscript. Running the six Jupyter Notebooks (`.ipynb`) sequentially (skipping the script `06_aggregate_scores.py`) allows the user to reproduce results from the manuscript, including data preparation, model training, and evaluation, using a subset of the full data (specifically, the publicly available annotated [dataset](https://doi.org/10.5061/dryad.9s4mw6mn3)). The results figures of the manuscript can be produced by directly running `07_explore_results.ipynb` without running any previous steps. Specific instructions for running these notebooks is given below. 

Notebooks and scripts included in this repository: 

- `01_explore_annotated_data.ipynb` Explore annotated dataset of _Rana sierrae_ call types

- `02_prep_training_data.ipynb` Prepare annotated files for training a CNN machine learning model

- `03_train_cnn.ipynb` Train a CNN to recognize Rana sierrae vocaliztaions

- `04_cnn_prediction.ipynb` Use the cnn to detect Rana sierrae in audio recordings

- `05_cnn_validation.ipynb` Analyze the accuracy and performance of the CNN

- `06_aggregate_scores.py` Aggregate scores from CNN prediction across dates and times of day. Note that this script is only provided as a demonstration of aggregating scores from a large dataset. Since we do not include the full audio dataset (thousands of hours of audio) or full set of CNN prediction across the entire audio dataset, the outputs of this script cannot be reproduced with the provided data. Instead, we include the outputs of this script (summaries of call activity detected by the CNN) as data tables in this repository. If you are running these notebooks sequentially, simply skip this script and proceed from `05_cnn_validation.ipynb` to `07_explore_results.ipynb`. 

- `07_explore_results.ipynb` Analyze temporal patterns of vocal activity using the CNN detections

## Running the code in this repository

To use these notebooks, first create a Python environment containing the required packages. We recommend using Anaconda, but feel free to use another virtual environment manager (e.g. `virtualenvwrapper`) if desired.

* Install Anaconda if you don't already have it.
   * Download the installer [here](https://www.anaconda.com/products/individual), or
   * follow the [installation instructions](https://docs.anaconda.com/anaconda/install/) for your operating system.
* Navigate to this folder in your command line (eg, `cd /path/to/rana-sierrae-cnn`)
* Create a Python conda environment containing the required packages: `conda env create -f conda_environment.yml --name rana_sierrae`

These notebooks use the Python package OpenSoundscape version 0.8.0. (which can be installed in a Python environment with `pip install opensoundscape==0.8.0`. Note that the notebooks might not be fully compatible with other versions of OpenSoundscape. 

Questions regarding the analysis, data availability, or adaptation of this code for other purposes can be directed to Sam Lapp (sam.lapp@pitt.edu). 
