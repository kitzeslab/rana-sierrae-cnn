"""Generate CNN prediction scores for the entire dataset of aquatic soundscape recordings

This script uses the CNN trained in 03_train_cnn.py to detect Rana sierrae vocalizations in field recordings.

Note that the github repository does not contain the full (very large) table of CNN outputs nor the full original audio
dataset, and thus does not contain the files needed to reproduce the outputs of this script. 

Instead, this script demonstrates the prediction process by generating CNN scores on the validation set.
"""
from opensoundscape.torch.models.cnn import load_model
import wandb
from pathlib import Path
from datetime import datetime
import pandas as pd
from torch import softmax, tensor

# initialize a weights and biases session to track progress during this prediction task
wandb_session = wandb.init(
    entity='kitzeslab',
    project="ecco12_ramu_predict",
    name='predict_sine2022a',
)

# choose output location for saving .csv files of CNN output scores
score_save_dir = './resources/'

# load the OpenSoundscape CNN model object
model = load_model('./resources/rana_sierrae_cnn.model')

# generate a list of all folders containing audio data to run predictions on
# for this example we should make it the validation set #TODO
audio_folders = ['./resources/field_data/']

# TODO: update the model version to opso 0.8.0
validation_df = pd.read_csv('./resources/validation_set.csv').set_index(['file','start_time','end_time'])

# generate predictions using batch size 1024
scores, _, unsafe_samples = model.predict(validation_df,num_workers=12,batch_size=1024,wandb_session=wandb_session)
# compute the softmax score across the two classes
scores['softmax']=softmax(tensor(scores[['ramu','negative']].values),1)[:,0].numpy()

# save scores to file along with labels
validation_df['score']=scores['softmax']

validation_df[['ramu','score']].to_csv('./resources/validation_labels_and_scores.csv')

# let wandb know that this task finished successfully
wandb_session.finish()

#TODO: save validation set scores to ./resources/validation_labels_and_scores.csv
