
import torch

from model.validate import validate

from icecream import ic



def train(model,batch,optimizer,device):
    
    """
    Calculates and returns the loss for the given batch.
    
    Parameters
    ----------
    model: torchvision.models.detection.faster_rcnn.FasterRCNN
        Model
    batch: tuple
        Batch
    optimizer: torch.optim
        Optimizer
    device: torch.device
        Device
        
    Returns
    -------
    loss: torch.Tensor
        Loss
        
    """
    
    X,Y = batch
    X = [x.to(device) for x in X]
    Y = [{k:v.to(device) for k,v in y.items()} for y in Y]
    
    # ic("to device")
    
    # print(Y)
    # quit()
    
    model.to(device)
    model.train()
    
    
    optimizer.zero_grad()
    losses = model(X,Y)


    loss = sum(loss for loss in losses.values())/len(X)
    

    loss.backward()
    optimizer.step()
    
    return loss    
    
    
    
def train_rccn(model,optimizer,train_dataloader,validation_dataloader,
               device,epochs=10,verbose=True):
    
    
    
    print("Training the model...\n")
    """
    Trains the model.
    
    Parameters
    ----------
    model: torchvision.models.detection.faster_rcnn.FasterRCNN
        Model
    optimizer: torch.optim
        Optimizer
    train_dataloader: torch.utils.data.DataLoader
        Train dataloader
    validation_dataloader: torch.utils.data.DataLoader
        Validation dataloader
    device: torch.device
        Device
    epochs: int
        Number of epochs
    verbose: bool
        If True, prints the loss for each epoch
        
    Returns
    -------
    None
    
    """
    
    
    # ic(len(train_dataloader))
    n_train_batches = len(train_dataloader)
    for i in range(1,epochs+1):


            
        iteration_train_loss = []
        
        for i_batch, batch in enumerate(train_dataloader):
            

            try:
                train_loss = train(model=model,
                               batch=batch,
                               optimizer=optimizer,
                               device=device)
                # print(train_loss)
            except Exception as e:
                print(e)
                continue
            iteration_train_loss.append(train_loss.item())
            
            mean_train_loss = round(sum(iteration_train_loss)/len(iteration_train_loss),4)

            ic(f"{i_batch} / {n_train_batches} Training loss: {mean_train_loss}\n")
            
        iteration_validation_loss = []
        
        for _,batch in enumerate(validation_dataloader):
            
            try:
                
                validation_loss = validate(model=model,
                                        batch=batch,
                                        device=device)
                iteration_validation_loss.append(validation_loss.item())
            except Exception as e:
                print(e)
                continue
            
        mean_train_loss = round(sum(iteration_train_loss)/len(iteration_train_loss),4)
        mean_validation_loss = round(sum(iteration_validation_loss)/len(iteration_validation_loss),4)
        
        # if verbose:
        
        print(f"{i} / {epochs}, train_loss: {mean_train_loss}, validation_loss: {mean_validation_loss}\n")
            