# Automated detection of _Rana sierrae_ vocalizations

This repository contains scripts related to the analyses and methods of a manuscript accepted for publication in The American Naturalist:

> Lapp, S., Smith, T. C., Wilhelm, A, Knapp, R., Kitzes, J. _In press_. Aquatic soundscape recordings reveal diverse vocalizations and nocturnal activity of an endangered frog. The American Naturalist.

Manuscript Abstract:
> Autonomous sensors provide opportunities to observe organisms across spatial and temporal scales that are not possible with direct human observation. By processing large data streams from autonomous sensors with deep learning methods, researchers can make novel and important natural history discoveries. In this study, we combine automated acoustic monitoring with deep learning models to observe breeding-associated activity in the endangered Sierra Nevada yellow-legged frog (Rana sierrae), behavior that current surveys do not measure. By deploying inexpensive hydrophones and developing a deep learning model to recognize breeding-associated vocalizations, we discover three undocumented R. sierrae vocalization types and find an unexpected temporal pattern of nocturnal breeding-associated vocal activity. This study exemplifies how the combination of autonomous sensor data and deep learning can shed new light on species’ natural history, especially during times or in locations where human observation is limited or impossible.

This repository uses an open-source dataset of annotated _Rana sierrae_ vocalizations from aquatic soundscape recordings. That dataset is available on Dryad: 

> Lapp, Sam; Kitzes, Justin (2023), Rana sierrae annotated aquatic soundscapes 2022, Dryad, Dataset, https://doi.org/10.5061/dryad.9s4mw6mn3

The repository contains six notebooks and one script which each demonstrate one step of the analyses described in the manuscript. Running the six Jupyter Notebooks (`.ipynb`) sequentially (skipping the script `06_aggregate_scores.py`) allows the user to reproduce results from the manuscript, including data preparation, model training, and evaluation, using a subset of the full data (specifically, the publicly available annotated [dataset](https://doi.org/10.5061/dryad.9s4mw6mn3)). The results figures of the manuscript can be produced by directly running `07_explore_results.ipynb` without running any previous steps. Specific instructions for running these notebooks is given below. 

## Notebooks and scripts included in this repository: 

Each Jupyter Notebook and python script can be run and modified (see instructions below), but we also provide static HTML renderings of each notebook (.html files in `./html_notebooks` subfolder) which can be opened in a web browser. These pages include code, figures, and interactive audio widgets allowing the user to view spectrograms and listen to sounds. 

- `01_explore_annotated_data.ipynb` Explore annotated dataset of _Rana sierrae_ call types

- `02_prep_training_data.ipynb` Prepare annotated files for training a CNN machine learning model

- `03_train_cnn.ipynb` Train a CNN to recognize Rana sierrae vocaliztaions

- `04_cnn_prediction.ipynb` Use the cnn to detect Rana sierrae in audio recordings

- `05_cnn_validation.ipynb` Analyze the accuracy and performance of the CNN

- `06_aggregate_scores.py` Aggregate scores from CNN prediction across dates and times of day. Note that this script is only provided as a demonstration of aggregating scores from a large dataset. Since we do not include the full audio dataset (thousands of hours of audio) or full set of CNN prediction across the entire audio dataset, the outputs of this script cannot be reproduced with the provided data. Instead, we include the outputs of this script (summaries of call activity detected by the CNN) as data tables in this repository. If you are running these notebooks sequentially, simply skip this script and proceed from `05_cnn_validation.ipynb` to `07_explore_results.ipynb`. 

- `07_explore_results.ipynb` Analyze temporal patterns of vocal activity using the CNN detections. This notebook reproduces the results figures in the manuscript. 

## Running the code in this repository

To use these notebooks, first create a Python environment containing the required packages. We recommend using Anaconda, but feel free to use another virtual environment manager (e.g. `virtualenvwrapper`) if desired.

* Install Anaconda if you don't already have it.
   * Download the installer [here](https://www.anaconda.com/products/individual), or
   * follow the [installation instructions](https://docs.anaconda.com/anaconda/install/) for your operating system.
* Navigate to this folder in your command line (eg, `cd /path/to/rana-sierrae-cnn`)
* Create a Python conda environment containing the required packages: `conda env create -f conda_environment.yml --name rana_sierrae`

These notebooks use the Python package OpenSoundscape version 0.8.0. (which can be installed in a Python environment with `pip install opensoundscape==0.8.0`. Note that the notebooks might not be fully compatible with other versions of OpenSoundscape. 

Questions regarding the analysis, data availability, or adaptation of this code for other purposes can be directed to Sam Lapp (sam.lapp@pitt.edu). 


## Description of other files in this repository

The subdirectories `resources` and `figures` contain intermediate and ultimate outputs from the analyses performed by the Python notebooks and scripts. Each file is described below:

### CSV Tables in ./resources/
- `audio_and_raven_files.csv`: Contains the file names for each file in the annotated dataset. The `audio` column contains the file name of the audio file and the `raven` column contains the file name of the raven column. This table is used in Notebooks 1 and 2. 
- `cnn_validation_outputs.csv`: Contains the predicted scores from the trained Rana sierrae recognizer (CNN) for each clip in the validation set. Columns:
   - file
   - start_time: time in seconds of the clip from the start of the file
   - end_time: time in seconds of the end of the 2 second clip from the start of the file
   - ramu: CNN's prediction of _Rana sierrae_ presence
   - negative: CNN's prediction of _Rana sierrae_ absence
   - softmax: the softmax score for _Rana sierrae_ presence calculated by combining the previous two columns; takes values between 0 and 1
- `detection_by_date.csv`: Table of the number of CNN detections of _Rana sierrae_ across dates in the full field dataset (not just the publicly available annotated dataset), for various thresholds. A detection is one two second clip with a score above the threshold. Column names are for date and six score thresholds: 2, 4, 6, 7.313 (threhsold used in manuscript main body results), 8, and 10. The score used is the logit of the softmax score. 
- `detections_by_time.csv`: Table of the number of CNN detections of _Rana sierrae_ across times of day in the full field dataset (not just the publicly available annotated dataset), for various thresholds. A detection is one two second clip with a score above the threshold. Column names are for date and six score thresholds: 2, 4, 6, 7.313 (threhsold used in manuscript main body results), 8, and 10. The score used is the logit of the softmax score. 
- `dvar_by_time.csv`: Table of the detected vocal activity rate (DVAR) of CNN detections of _Rana sierrae_ across times of day in the full field dataset (not just the publicly available annotated dataset), for various thresholds. DVAR is calculated as the fraction of 2 second clips with a detection for a given time period. A detection is one two second clip with a score above the threshold. Column names are for date and six score thresholds: 2, 4, 6, 7.313 (threhsold used in manuscript main body results), 8, and 10. The score used is the logit of the softmax score. 
- `dvar_by_card_and_date.csv`: Equivalent to `dvar_by_time.csv` but with an additional level of categorization, by the recording device (here named by the "card" ie SD card on which the data was recorded). The card column's values correspond to one of the five recording devices. 
- `labels_2s.csv`: Annotations (labels) for every 2-second segment of the files in the public annotated dataset. Annotations are given for each of 5 call types (columns are named for call types). A 1 indicates the call type is present in that 2-second clip. 
- `total_detections_per_threshold.csv`: summary of total number of detected vocalizations at each threshold. Values in first column correspond to score thresholds : 2, 4, 6, 7.313 (threhsold used in manuscript main body results), 8, and 10. The score used is the logit of the softmax score. 
- `training_set.csv` and `validation_set.csv`: these are subsets of `labels_2s.csv` which represent a split of labels to be used for training and validation of the CNN. Each row in `labels_2s.csv` is in either `training_set` or `validation_set`. The `rana_sierrae` has a value of 1 if either A or E type calls are present, since these are the two calls the CNN is trained to detect. 
- `validation_labels_and_scores.csv`: combines the `validation_set.csv`'s `rana_seirra` column (1 for present, 0 for absent) with the `cnn_validation_outputs.csv`'s CNN prediction scores for each clip. The score stored in this column is the softmax; a logit operation is applied before using the thresholds mentioned above. 

### Model file in ./resources/
`rana_seirrae_cnn.model` is a saved CNN model object that can be loaded in opensoundscape v0.8.0 with the `load_model()` function. It is the original model trained and used during the analysis reported in the manuscript, and can be used to recreated the exact results produced in the mansucript (as shown in Notebook 7). 

### Figures in ./figures
The figures are produced within the `.ipynb` Notebooks. 

Three figures (`vocal_activity_annotated_7_days.pdf`, `daily_pattern_separate_days.pdf`, and `daily_patterns_by_call_type_annotated.pdf`) summarize temporal activity patterns from just the annotated dataset. 

Two figures (`precision_and_recall_vs_threshold.pdf` and `precision_recall_curve.pdf`) visualize the performance of the classifier on the validation set by plotting precision and recall metrics. 

The remaining figures summarize the detections of the CNN on the full field dataset collected for the study:
- `dvar_by_card.pdf`: Detected Vocal Activity Rate (defined above) for each device, by date across the full recording period
- `seasonal_activity_normalized_thresholds.pdf` plots the same seasonal trend as `dvar_by_card` for each detetion threshold, with each curve normalized by the area under the curve (total detections at that threshold). This demonstrates that though different thresholds result in different numbers of detections, the temporal patterns are consistent regardless of threshold choice. 
- `time_with_3hr_rolling_avg_thresholds.pdf`: Plots the detected vocal activity rate (defined above) calculated on a 15 minute basis with a 3 hour moving average applied, across the day, for all recording dates. 
