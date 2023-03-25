from opensoundscape.audio import Audio
from opensoundscape.spectrogram import Spectrogram

import numpy as np
import pandas as pd
from glob import glob
from pathlib import Path

from opensoundscape.torch.models.cnn import CNN
from opensoundscape.preprocess.preprocessors import SpectrogramPreprocessor
from opensoundscape.data_selection import resample
import wandb

name = 'm2'

# Train on A and V classes, excluding X class

labels = pd.read_csv('/media/emu/datasets/labeled/ramu_10s_msd0558/labels_2s.wav')

#choose training and validation labels
labels['ramu']=np.logical_or(labels.A,labels.V).astype(int)

# drop clips with 0 for ramu and 1 for 'X' unsure class
labels = labels.drop(labels[(labels.ramu==0) & (labels.X==1)].index)


from sklearn.model_selection import train_test_split

train_files,val_files = train_test_split(labels.audio_file.unique(),test_size=0.1,random_state=20221208)

labels=labels.rename(columns={'audio_file':'file'})
labels = labels.set_index('file')
train_df = labels.loc[train_files]
val_df = labels.loc[val_files]

train_df = train_df.reset_index().set_index(['file','start_time','end_time'])[['ramu']]
train_df['negative']=1-train_df.ramu
val_df = val_df.reset_index().set_index(['file','start_time','end_time'])[['ramu']]
val_df['negative']=1-val_df.ramu

# upsample to match the class with the most samples (reuse samples from other classes)
train_df = resample(train_df,upsample=True,n_samples_per_class=train_df.sum().max())

wandb_session = wandb.init(
    entity='kitzeslab',
    project="ecco12_ramu",
    # name='ramu_A',
    config=dict(
        comment="Description: training binary resnet18 on A+V classes and excluding unknown class X",
    )
)

model = CNN(architecture='resnet18',classes=train_df.columns,sample_duration=2.0,single_target=True)
model.preprocessor.pipeline.bandpass.set(min_f=300,max_f=2000)
model.preprocessor.pipeline.frequency_mask.set(max_masks=5,max_width=0.1)
model.preprocessor.pipeline.time_mask.set(max_masks=5,max_width=0.1)
model.preprocessor.pipeline.add_noise.set(std=0.01)

model.optimizer_params['lr']=0.002

model.train(
    train_df,
    val_df,
    epochs=20,
    batch_size=128,
    num_workers=12,
    save_path=f'/media/emu/projects/sml161/ecco12_ramu/trained_models/{name}',
    save_interval=1,
    log_interval=10,
    validation_interval=1,
    wandb_session=wandb_session
)
wandb_session.finish()