import torch
from icecream import ic 
import numpy as np

@torch.no_grad()
def predict(image,model_path=None,model=None):
    
    """
    Returns prediction for the given image.
    
    Parameters
    ----------
    image: torch.Tensor
        Image
    model_path: str
        Path to the model
    model: torch.nn.Module
        Model
        
    Returns
    -------
    prediction: torch.Tensor
        Prediction
    """
    
    model = torch.load(model_path) if model is None else model
    
    model.eval()
    prediction = model(image)
    
    return prediction
    
    
    
    
    
    





@torch.no_grad()
def predict_all(device,model_path=None,model=None,batch=None,test_root="../DATA/Data/test",batch_size=2,threshold=0.3):
    
    
    """
    Returns predictions for all images in the test directory or for the given batch.
    
    Parameters
    ----------
    device: torch.device
        Device
    model_path: str
        Path to the model
    model: torch.nn.Module
        Model
    batch: torch.Tensor
        Batch
    test_root: str
        Path to the test directory
    threshold: float
        Threshold for the scores
        
    Returns
    -------
    finall_predictsions: list
        List of predictions
    """
    
    
    model = torch.load(model_path) if model is None else model
    
    X, Y = batch
    X = [x.to(device) for x in X]

    with torch.no_grad():
        predictions = model(X)


    finall_predictsions = []
    for i in range(len(X)):
        
        boxes, scores, labels = [predictions[i][key].cpu().numpy() for key in ['boxes', 'scores', 'labels']]
              
        indecies = np.where(scores>threshold)
        
        if len(indecies[0]) == 0:
            continue
        boxes = boxes[indecies]
        scores = scores[indecies]
        labels = labels[indecies]
        
 
        finall_predictsions.append((boxes,scores,labels))
        
    return finall_predictsions
        
