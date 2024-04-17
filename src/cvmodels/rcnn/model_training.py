import torch
from torch.utils.data import DataLoader

import sys
sys.path.append('./rcnn')
import os

from rcnn.train import train_rccn
from rcnn.model import faster_rccn
from rcnn.dataset import RCNN_Dataset
from helper_functions.collate import collate_fn
from icecream import ic

import warnings
warnings.filterwarnings('ignore')



def train_model(model,batch_size=4,lerning_rate=0.001,
                epochs=30,mode_save_root='trained_models',
                optimizer=None,
                TRAIN_ROOT = "../DATA/Data/train",
                VALIDATION_ROOT = "../DATA/Data/validation",
                ANNOTAION_PATH = "../DATA/Data_COCO/annotations.coco.json",
                trainable_backbone_layers=3):
    

    """
    Train the model. Trains the model and saves it to the given directory.
    
    Parameters
    ----------
    batch_size: int
        Batch size
    lerning_rate: float
        Learning rate
    epochs: int
        Number of epochs
    mode_save_root: str
        Path to the directory to save the model
    optimizer: torch.optim
        Optimizer
    TRAIN_ROOT: str
        Path to the train data root
    VALIDATION_ROOT: str
        Path to the validation data root
    ANNOTAION_PATH: str
        Path to the annotation file
    model: torchvision.models.detection.faster_rcnn.FasterRCNN
        Model to train
    trainable_backbone_layers: int
        Number of trainable backbone layers
    
    
    Returns
    -------
    None
    """

    train_set = RCNN_Dataset(image_directory=TRAIN_ROOT,annotation_file_path=ANNOTAION_PATH)
    validation_set = RCNN_Dataset(image_directory=VALIDATION_ROOT,annotation_file_path=ANNOTAION_PATH)


    train_dataloader = DataLoader(dataset=train_set,batch_size=batch_size,shuffle=True,collate_fn=collate_fn)
    validation_dataloader = DataLoader(dataset=validation_set,batch_size=batch_size,shuffle=True,collate_fn=collate_fn)




    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    model = faster_rccn(trainable_backbone_layers=trainable_backbone_layers) if model is None else model

    optimizer = torch.optim.Adam(model.parameters(),lr=lerning_rate) if optimizer is None else optimizer



    if not os.path.exists(mode_save_root):
        os.mkdir(mode_save_root)
        
    model_save_path = os.path.join(mode_save_root,'rcnn_'+str(epochs)+ '_epoch_trained.pth')


    torch.cuda.empty_cache()

    train_rccn(model=model,optimizer=optimizer,
            train_dataloader=train_dataloader,
            validation_dataloader=validation_dataloader,
            device=device,
            epochs=epochs)


    torch.save(model,model_save_path)