""""
In this file, we will define a function that will be used to split the data into training, validation and testing sets.
Also, we will define a function to split data for each class. This make the project more organized and flexible.

"""


import os
import shutil
import json
from copy import deepcopy


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
    
    
    
def resplit_by_nnps(root,full_annotations_path,dest_root):
    
    
    """
    
    ['Natural', 'Negative', 'Positive', 'Surprise']
    
    """
    
    nnps_maping = {        
              "Happy":"Positive",
              "Surprise":"Surprise",
              "Natural":"Natural",
              "Angry":"Negative",
              "Sad":"Negative",
              "Disgust":"Negative",
              "Boredom":"Negative",
              "Confusion":"Negative",
              "Frustration":"Negative",
              "Engaged":"Positive",
              "Yawning":"Negative",
              "Sleepy":"Negative"}
    
    # new category mapping 
    new_cat_map = {"Negative":0,
                   "Positive":1,
                   "Natural":2,
                   "Surprise":3}
    
    
    
    

    nnps_annotations = []
    nnps_images = []
    
    # new categories
    nnps_categories = [{"id":value,"name":key,"supercategory":'none'} for key,value in new_cat_map.items()]
    
    
    with open(full_annotations_path,'r') as f:
        
        annotations = json.load(f)
        
        annotation = annotations['annotations']
        categories = annotations['categories']
        images = annotations['images']
        
        # print(images[0])
        # quit()
        # print(categories)

        # new category mapping: numberical format
        cat_id_to_name = {cat['id']:cat['name'] for cat in categories}
        cat_name_to_id = {cat['name']:cat['id'] for cat in categories}
        # print(cat_name_to_id)
        
        new_cateogry_mapping = {}
        
        for cat in nnps_maping:
            
            try:
                ID = cat_name_to_id[cat]
            except:
                pass
            
            new_cat = nnps_maping[cat]
            new_cat_id = new_cat_map[new_cat]
            
            new_cateogry_mapping[ID] = new_cat_id       
            

        
        n_annotations = len(annotation)
        
        # iterate over all annotations to create new dataset and also change annotations
        # we need only images and annotations that are part of nnps_mapping, so, there is performing label concatination
        # what we are doing, we are creating new dataset, where labels are combined into 4 categories
        
        # to avoid image duplication, we need to track the image id and add it to the new dataset if it is not already added
        image_ids = []
        for i in range(n_annotations):
            
            ann = deepcopy(annotation[i])
            
            try:
                
                ann['category_id'] = new_cateogry_mapping[ann['category_id']]
                image_id = ann['image_id']
                
                if image_id not in image_ids:
                
                    # print(image_id)
                    image = [img for img in images if img['id'] == image_id][0]
                    image_ids.append(image_id)
                    nnps_images.append(image)

                                
                nnps_annotations.append(ann)
            except:
                pass
        print(f"Total labels: {n_annotations}")
        print(f"Total labels after nnps mapping: {len(nnps_annotations)}")
        print(f"Total images: {len(images)}")
        print(f"Total images after nnps mapping: {len(nnps_images)}")
            
        # quit()
        nnps_annotations_dict = {'annotations':nnps_annotations,'images':nnps_images,'categories':nnps_categories}
        
        
        # save annotations to the destination folder
        image_dir = os.path.join(dest_root,"nnps_full_images")

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        else:
            answer = input(f"{image_dir} already exists. Do you want to overwrite it? (y/n) ")
            
            if answer == 'y':
                shutil.rmtree(image_dir)
                os.makedirs(image_dir)
                
        with open(dest_root+'/nnps_annotations.json','w') as f:
            json.dump(nnps_annotations_dict,f)
            


    
        # copy images to the destination folder
        for image in nnps_images:
            
            image_path = os.path.join(root,image['file_name'])
            dest_path = os.path.join(image_dir,image['file_name'])
            
            try:
                shutil.copy(image_path,dest_path)     
            except:
                print(f"Failed to copy {image_path} to {dest_path}")
    
    
