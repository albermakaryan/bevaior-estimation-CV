""""
In this file, we will define a function that will be used to split the data into training, validation and testing sets.
Also, we will define a function to split data for each class. This make the project more organized and flexible.

"""


import os
import shutil
import json


def resplit_by_label(root,annotatsions,dest_root):
    
    
    with open(annotatsions,'r') as f:
        
        annotatsions = json.load(f)
        

        images = annotatsions['images']
        categories = annotatsions['categories']
        
        category_id_to_name = {cat['id']:cat['name'] for cat in categories}
        
        categories_for_dataset = {cat:[] for cat in category_id_to_name}
        # for multiple categories
        categories_for_dataset[11111] = []
        category_id_to_name[11111] = 'MultLabel'

        
        n_images = len(images)
        
        for i in range(n_images):
            
            
            image = images[i]
            image_filename = image['file_name']
            image_id = image['id']
            image_annotations = [ann for ann in annotatsions['annotations'] if ann['image_id'] == image_id]
            
            # if image is multilabel, add it to the multilabel category
            image_categories = list({ann['category_id'] for ann in image_annotations})
            
            image_category_id = image_categories[0] if len(image_categories) == 1 else 11111
            
            # print(image_annotations)
            # continue
            
            categories_for_dataset[image_category_id].append(image_filename)
            # print(image_annotations)
            
        # quit()
        # print({id:len(value) for id, value in categories_for_dataset.items()})   
        
        # save the images to the destination folder
        for category_id,images in categories_for_dataset.items():
            
            category_name = category_id_to_name[category_id]
            category_folder = os.path.join(dest_root,category_name)
            
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)
            else:
                answer = input(f"{category_folder} already exists. Do you want to delete it? (y/n) ")
                
                if answer == 'y':
                    shutil.rmtree(category_folder)
                    os.makedirs(category_folder)
                
                
            for image in images:
                
                image_path = os.path.join(root,image)
                dest_path = os.path.join(category_folder,image)
                
                try:
                    shutil.copy(image_path,dest_path)     
                except:
                    print(f"Failed to copy {image_path} to {dest_path}")
    print('Data has been splitted by label')
    
    