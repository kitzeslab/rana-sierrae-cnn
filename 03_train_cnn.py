"""Train a deep learning model (CNN) to recognize Rana sierrae vocalizations in audio recordings

This script uses the training and validation data generated in 02_prep_training_data.ipynb to train
a CNN using OpenSoundscape. 

Note that training is a stochastic process and will result in slightly different results each time
the script is run. The original model object trained and used in the manuscript is included in 
the subfolder `./resources`. 
"""
import pandas as pd
from opensoundscape.torch.models.cnn import CNN
from opensoundscape.data_selection import resample
import wandb

# Load the training and validation datasets prepared in the notebook 02_prep_training_data.ipynb
train_df = pd.read_csv('./resources/training_set.csv').set_index(['file','start_time','end_time'])
train_df['negative']=1-train_df.ramu
val_df = pd.read_csv('./resources/validation_set.csv').set_index(['file','start_time','end_time'])
val_df['negative']=1-val_df.ramu

# upsample to match the class with the most samples (reuse samples from other classes)
train_df = resample(train_df,upsample=True,n_samples_per_class=train_df.sum().max())

# initialize Weights and Biases logging session for tracking model training progress
wandb_session = wandb.init(
    entity='kitzeslab',
    project="ecco12_ramu",
    config=dict(
        comment="Description: training binary resnet18 on A+V classes and excluding unknown class X",
    )
)

# create opensoundscape.CNN object to train a CNN on audio
model = CNN(architecture='resnet18',classes=train_df.columns,sample_duration=2.0,single_target=True)

#modify preprocessing of the CNN:
#bandpass spectrograms to 300-2000 Hz
model.preprocessor.pipeline.bandpass.set(min_f=300,max_f=2000)
#modify augmentation routine parameters
model.preprocessor.pipeline.frequency_mask.set(max_masks=5,max_width=0.1)
model.preprocessor.pipeline.time_mask.set(max_masks=5,max_width=0.1)
model.preprocessor.pipeline.add_noise.set(std=0.01)

# increase the learning rate from the default value
model.optimizer_params['lr']=0.002

# train CNN for 20 epochs with batch size 128
model.train(
    train_df,
    val_df,
    epochs=20,
    batch_size=128,
    num_workers=12,
    save_path=f'/media/emu/projects/sml161/ecco12_ramu/trained_models/m2',
    save_interval=1,
    log_interval=10,
    validation_interval=1,
    wandb_session=wandb_session
)
#let wandb know this run finished successfully
wandb_session.finish()