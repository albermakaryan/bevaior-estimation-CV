"""
The main data engineering tasks have been done using coco format dataset. 
In this file, we are going to define functions to helps us to make a dataset appropriate for training different models.
"""

import os
import shutil
import json
import yaml
from functions import get_image_annotations, make_category_annotation_row


def convert_to_yolo(source_root,dest_root,annotations_path):
    
    
    if  os.path.exists(dest_root):
        answer = input("The destination folder already exists. Do you want to overwrite it? (y/[something else]]) ")
        
        if answer.lower() == 'y':
            shutil.rmtree(dest_root)
            os.makedirs(dest_root)
            
        else:
            print("Exiting")
            return
        
    else:
        os.makedirs(dest_root)
                       
                       
    
    with open(annotations_path,'r') as file:
        
        full_annotations = json.load(file)
        
        annotations = full_annotations['annotations']
        
        images = full_annotations['images']
        
        
        n_images = len(images)
        
        for i in range(n_images):
            
            print(f"{'-_-'*20}{i+1}/{n_images}{'-_-'*20}")

            
            # if i < 10:
                # continue
            
            image = images[i]
            
            image_id = image['id']
            image_filename = image['file_name']
            label_folder = os.path.join(dest_root,'labels')
            
            if not os.path.exists(label_folder):
                os.makedirs(label_folder)
                

                
            label_path = os.path.join(label_folder,image_filename.replace('.jpg','.txt'))

            
            image_annotationes = get_image_annotations(image_id,annotations)
            
            # new_format_annotationess = [make_category_annotation_row(ann,image) for ann in image_annotationes]
            
            # save
            
            with open(label_path,'w') as file:
                
                for ann in image_annotationes:
                    
                    catgeroy_id,x1,y1,w,h = make_category_annotation_row(ann,image,scale=True)
                    
                    file.write(f"{catgeroy_id} {x1} {y1} {w} {h}\n")
                    
            image_source_path = os.path.join(source_root,image_filename)
            image_dest_path = os.path.join(dest_root,'images')
            
            if not os.path.exists(image_dest_path):
                os.makedirs(image_dest_path)
                
            image_dest_path = os.path.join(image_dest_path,image_filename)
            
            shutil.copy(image_source_path,image_dest_path)
                    

    
    pass



def convert_all_sets(source_root,dest_root):
    
    for set_name in ['train','valid','test']:
        
        source_folder = os.path.join(source_root,set_name)
        dest_folder = os.path.join(dest_root,set_name)
        annotations_path = os.path.join(source_root,set_name,'_annotations.json')
        convert_to_yolo(source_folder,dest_folder,annotations_path)
    
    
if __name__ == "__main__":
    
    convert_all_sets(source_root='../data/model_data/nnps_coco_format/',
                     dest_root= '../data/model_data/nnps_yolo_format/')