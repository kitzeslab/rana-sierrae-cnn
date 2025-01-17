"""Aggregate scores from CNN prediction across dates and times of day

NOTE: the github repository does NOT contain the full (very large) table of CNN outputs nor the full original audio
dataset, and thus does not contain the files needed to reproduce the outputs of this script. The full set
of CNN output scores is available from the authors upon reasonable request. 

This script takes the raw predictions saved by the cnn prediction task (which saves csvs of output scores)
and summarizes the detected vocalizations across dates and times of day, using various thresholds. 

The files saved by this script are used in the subsequent notebook 07_explore_results.ipynb. 
"""
import numpy as np
import pandas as pd
from glob import glob
from scipy.special import softmax, logit
from opensoundscape.audiomoth import audiomoth_start_time
import pytz

# load score tables produced by prediction on field data, and aggregate into one table:
# Note that the full prediction tables are not included in this repository. They are available upon reasonable reqest.
scores = pd.concat([pd.read_csv(f) for f in glob('prediction/output/dir/preds*.csv')])
thresholds = [2,4,6,7.313,8,10]
threshold_columns = [f"t_{th}" for th in thresholds]

# generate the softmax score across the two classes
scores['sm']=softmax(scores[['rana_sierrae','negative']],axis=1)[:,0]

# generate the logit of the softmax score
scores['lg']=logit(scores['sm'])

# parse the card name (card corresponds to recorder) for each file
scores['card']=[f.split('/')[-2] for f in scores.file]

# add date and time objects to the score dataframe using the datetime and pytz libraries
tz = pytz.timezone('US/Pacific') #local timezone of the field deployment
scores['date']=[audiomoth_start_time(f).astimezone(tz).date() for f in scores.file]
scores['time']=[audiomoth_start_time(f).astimezone(tz).time() for f in scores.file]

# in a few files, there's an extra 1 second at the end of the time stamp, eg 12:33:01
# we'll replace that with a truncated minute time stamp like 12:33:00
scores['time']=[d.replace(second=0) for d in scores['time']]

#create 0/1 detection history based on various thresholds and the CNN output scores
for th in thresholds:
    scores[f"t_{th}"] = scores.lg>th

dates = np.sort(scores.date.unique())
times = np.sort(scores.time.unique())

# summarize total number of detections at each score threshold
total_detections = pd.DataFrame(scores[threshold_columns].sum(),columns=['count'])
total_detections.index.name='threshold'
total_detections.to_csv('./resources/total_detections_per_threshold.csv')

#summarize total detections per date
date_total = scores.groupby('date').sum()
date_total[threshold_columns].to_csv('./resources/detections_by_date.csv')

# summarize mean detections per dates for each card
scores_card_date=scores.groupby(['card','date']).mean()[threshold_columns]
scores_card_date.to_csv('./resources/dvar_by_card_and_date.csv')

# summarize total detections per time of day
time_total = scores.groupby('time').sum()
time_total[threshold_columns].to_csv('./resources/detections_by_time.csv')

# summarize mean detections per time of day
time_total = scores.groupby('time').mean()
time_total[threshold_columns].to_csv('./resources/dvar_by_time.csv')