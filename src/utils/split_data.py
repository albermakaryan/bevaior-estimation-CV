import os
import shutil
import numpy as np
from functions import get_image_annotations
import json


def train_valid_test_split(image_root,annotation_file,dest_path,train_size=.8, valid_size=.1,random_state=123):
    
    
    if not os.path.exists(dest_path):
        
        os.makedirs(dest_path)
        
    else:
        answer = input("The destination folder already exists. Do you want to overwrite it? (y/[something else]]) ")
        
        if answer.lower() == 'y':
            shutil.rmtree(dest_path)
            os.makedirs(dest_path)
        else:
            print("Exiting")
            return
        
        
    with open(annotation_file,'r') as file:
        
        full_annotations = json.load(file)
        
        
        annotations = full_annotations['annotations']
        images = full_annotations['images']
        categories = full_annotations['categories']
        
        n_images = len(images)
        n_annotations = len(annotations)

        train_size = int(n_annotations*train_size)
        valid_size = int(n_annotations*valid_size)
        test_size = n_images - train_size - valid_size
        
        # shuffle the images
        np.random.seed(random_state)
        np.random.shuffle(images)
        
        
        new_annotations = {'train':[],'valid':[],'test':[]}
        new_images = {'train':[],'valid':[],'test':[]}
        
        
        annotation_tracker = 0
        
        for i in range(n_images):
            
            print(f"{'-_-'*20}{i+1}/{n_images}{'-_-'*20}")
            
            image = images[i]
            
            image_id = image['id']
            image_filename = image['file_name']
            
            image_annotations = get_image_annotations(image_id,annotations)
            annotation_tracker += len(image_annotations)
            
            if annotation_tracker < train_size:
                dest = 'train'
            elif annotation_tracker < train_size + valid_size:
                dest = 'valid'
            else:
                dest = 'test'
                
            new_annotations[dest].extend(image_annotations)
            new_images[dest].append(image)
            
            source_folder = os.path.join(image_root,image_filename)
            
            # if os.path.exists(source_folder):
            #     print(f"Image {image_filename} does exist in the source folder")
            #     quit()
            dest_folder = os.path.join(dest_path,dest)
            
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
                
            dest_image_path = os.path.join(dest_folder,image_filename)
            

            shutil.copy(source_folder,dest_image_path)
        
        
        for key in new_annotations:
            
            with open(os.path.join(dest_path,key, '_annotations.json'),'w') as file:
                
                json.dump({'annotations':new_annotations[key],'images':new_images[key],'categories':categories},file)

    
    
    # for image 
    
if __name__ == "__main__":
    
    image_root = '../data/full_data/balanced_nnps/images'
    annotation_file = '../data/full_data/balanced_nnps/balanced_dataset_annotations.json'
    dest_path = "../data/model_data/nnps_coco_format/"
    
    train_valid_test_split(image_root=image_root,annotation_file=annotation_file,dest_path=dest_path,train_size=.8, valid_size=.1,random_state=123)