
import os 
import random
import shutil
import boto3

def split(source_root,dest_root,train_size=0.8,validation_size=0.1,random_seed=123,
          working_directory=None): 
    
    """
    
    Splits images from source root into three parts and saves each for given directory.
    Test size is calculated as 1 - train_size - validation_size.
    
    Parameters
    
    source_root: str
        Path to the source directory
    dest_root: str
        Path to the destination directory
    train_size: float
        Size of the train set
    validation_size: float
        Size of the validation set
    random_seed: int
        Random seed
    working_directory: str
        Path to the working directory
        
    Returns
    -------
    None
    
    """
    
    
    
    
    if working_directory is not None:
        os.chdir(working_directory)
    pass

    files = os.listdir(source_root)
    
    random.seed(random_seed)
    random.shuffle(files)
    
    train,validation,test = [os.path.join(dest_root,folder) for folder in ['train','validation','test']]
    roots = [train,validation,test]
    
    if any(os.path.exists(root) for root in roots):
        
        ask = input("The destination folders already exists. Do you want to continue? (y/n)")
        
        if ask == 'y':
            
            for root in roots:
                
                shutil.rmtree(root)
                os.makedirs(root)
                
    else:
            
            for root in roots:
                
                os.makedirs(root)
    
    files_sze = len(files)
    train_size = int(files_sze*train_size)
    validation_size = int(files_sze*validation_size)
    
    for i in range(files_sze):
        
        file = files[i]
        
        root = train if i < train_size else validation if i < train_size+validation_size else test
        
        srource_path = os.path.join(source_root,file)
        dest_path = os.path.join(root,file)
        
        shutil.copy(srource_path,dest_path)
        
