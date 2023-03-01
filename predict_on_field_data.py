from opensoundscape.torch.models.cnn import load_model
import wandb
from pathlib import Path
from datetime import datetime
from glob import glob 
from tqdm import tqdm

wandb_session = wandb.init(
    entity='kitzeslab',
    project="ecco12_ramu_predict",
    name='predict_sine2022a',
)

score_save_dir = '/media/emu/projects/sml161/ecco12_ramu/cnn_preds/sine2022a'

model = load_model('/media/emu/projects/sml161/ecco12_ramu/trained_models/m2/best.model')

cards = glob('/media/emu/datasets/aru/sine2022a/*SD*')

print(f"{datetime.now()}: Starting prediction")
for card in tqdm(cards):
    files = glob(f"{card}/*.WAV")
    print(f"{datetime.now()}: predicting on {len(files)} files from card {Path(card).name}")

    scores, _, unsafe_samples = model.predict(files,num_workers=12,batch_size=1024,wandb_session=wandb_session)
    scores.to_csv(f"{score_save_dir}/preds_{Path(card).name}.csv")

print(f"{datetime.now()}: Finished prediction")

wandb_session.finish()
