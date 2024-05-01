"""

In this files we will define the functions that will be used to concatenate the image datasets we have.
The datasets are:
    - The original dataset: https://universe.roboflow.com/face-recognition-ixqtg/emotion-detection-cwq4g
    - The augmented dataset: https://universe.roboflow.com/malaviya-national-institute-of-technology-jaipur-india-6e6jq/affective-states

The reasons why we are concatenating the datasetes are:
    - To increase the number of emotions in the dataset
    - To increase the diversity of the dataset
    - To increase the robustness of the model
    - To solve imbalanced dataset problem
    
In terms of storage efficiecy, we don't push datasets to the git repository. We only push the code and the urls of original datasets.
"""

import os
import shutil
import json
from copy import deepcopy




def concat_annotations(source_root,dest_root):
    
    # define the splits
    splits = ["train", "valid", "test"]
    # Get the list of all the images in the main dataset
    dirs = os.listdir(source_root)

    # quit()
    dirs = {d:[os.path.join(source_root, d,split) for split in splits] for d in dirs}
    

    # get the list of all the annotations files 
    annotations_files = {d:[[os.path.join(dir,file) for file in os.listdir(dir) if file.split(".")[-1] == "json"][0] for dir in dirs[d]] for d in dirs}

    # full_annotations = None
    full_annotations_for_each = {}


        
    # define a list to store the number of categories in each dataset
    prev_n_categories = []
    
    # define a list to store the images, annotations and categories for final full dataset
    total_images = []
    total_annotations = []
    total_catagories = []
    
    for dataset_ind,dir in enumerate(annotations_files):
        
 
        # besides the full dataset, we need to store the same information for each dataset
        total_images_for_each = []
        total_annotations_for_each = []

        annotations_path = annotations_files[dir]
        n_annotations = len(annotations_path)

        # categories for current dataset
        
        for ann_ind in range(n_annotations):
            
            ann_file = annotations_path[ann_ind]
            
            # for the first data set, category ids remain the same
            # but for each dataset after the first one, we need to increment the category ids
            # annotation and image ids changes for all subsets after the first subset
            # for example, if the first dataset is emotion_dataset, the cagegory ids will be the same for all the
            # subsets of its' annotations, but annotation ids and image ids will change for each subset of the dataset after the first one.
            # So, if the test is the frist subset, the annotation and iamge ids remain the same, but for train and valid, we need to incremeent the ids
            # for the datasets after the first one, category ids will be incremented by the number of categories in the previous dataset, and
            # annotation and image ids will be incremented like for the first dataset.
            
            with open(ann_file,'r') as file:
                
                ann = json.load(file)

                
                # to avoid original data being overwritten, we need to make a deep copy of the original data
                annotations_for_full_dataset = deepcopy(ann["annotations"])
                images_for_full_dataset = deepcopy(ann["images"])
                categories_for_full_dataset = deepcopy(ann["categories"])
                
                annotations_for_each_dataset = deepcopy(ann["annotations"])
                images_for_each_dataset = deepcopy(ann["images"])
                categories_for_each_dataset = deepcopy(ann["categories"])
                

                # break
                n_images = len(images_for_full_dataset)
                n_annotations = len(annotations_for_full_dataset)
                n_categories = len(categories_for_full_dataset)
                

                image_id_increment_for_full_full_dataset = len(total_images)
                annotation_id_increment_for_full_dataset = len(total_annotations)
                                    
                image_id_increment_for_each_dataset = len(total_images_for_each)
                annotation_id_increment_for_each_dataset = len(total_annotations_for_each)
                
                if dataset_ind == 0: # this means the first dataset
                    
                    category_increment = 0

                    
                else:
                    
                    # so, since for the first dataset we don't increment the category ids, we need to increment
                    # the cateogry ids for the datasets after the first one, and we increment it 
                    # by adding the sum of total categories in the previous datasets to the current category id
                    category_increment = sum(prev_n_categories)
                    
                    
                # above we have defined the increments for each id, now we need to increment the ids
                # for each image, annotation and category
                # also, for imaeges and categories, we need mapping dictionaries to use to change image and category ids in annotations
                # image id increment
                
                image_mapping_for_full_dataset = {}
                image_mapping_for_each_dataset = {}
                for image_ind in range(n_images):
                    
                    old_id = images_for_full_dataset[image_ind]['id']
                    
                    # full dataset
                    new_id_full = old_id + image_id_increment_for_full_full_dataset
                    image_mapping_for_full_dataset[old_id] = new_id_full
                    images_for_full_dataset[image_ind]['id'] = new_id_full

                    # for each dataset
                    new_id_each = old_id + image_id_increment_for_each_dataset
                    image_mapping_for_each_dataset[old_id] = new_id_each
                    images_for_each_dataset[image_ind]['id'] = new_id_each
                    
                # category id increment
                category_mapping_for_full = {}
                for category_ind in range(n_categories):
                        
                    old_id = categories_for_full_dataset[category_ind]['id']
                    
                    # full dataset
                    new_id_full = old_id + category_increment
                    new_id_for_full = old_id + category_increment
                    
                    
                    category_mapping_for_full[old_id] = new_id_full
                    categories_for_full_dataset[category_ind]['id'] = new_id_full
                    
                # annotation id increment
                for annotation_ind in range(n_annotations):
                    
                    old_ann_id = annotations_for_full_dataset[annotation_ind]['id']
                    old_image_id = annotations_for_full_dataset[annotation_ind]['image_id']
                    old_category_id = annotations_for_full_dataset[annotation_ind]['category_id']
                    
                    # full dataset
                    new_ann_id_full = old_ann_id + annotation_id_increment_for_full_dataset
                    new_image_id_full = old_image_id + image_id_increment_for_full_full_dataset
                    new_category_id_full = old_category_id + category_increment
                    # print(old_category_id,category_increment)
                    
                    annotations_for_full_dataset[annotation_ind]['id'] = new_ann_id_full
                    annotations_for_full_dataset[annotation_ind]['image_id'] = new_image_id_full
                    annotations_for_full_dataset[annotation_ind]['category_id'] = new_category_id_full
                    
                    # for each dataset
                    new_ann_id_each = old_ann_id + annotation_id_increment_for_each_dataset
                    new_image_id_each = image_mapping_for_each_dataset[old_image_id]
                    
                    annotations_for_each_dataset[annotation_ind]['id'] = new_ann_id_each
                    annotations_for_each_dataset[annotation_ind]['image_id'] = new_image_id_each
                    
                                            
                
                # extend lists to corresponding lists
                total_images.extend(images_for_full_dataset)
                total_annotations.extend(annotations_for_full_dataset)
                
                total_images_for_each.extend(images_for_each_dataset)
                total_annotations_for_each.extend(annotations_for_each_dataset)
                
                if ann_ind == 2:
                    total_catagories.extend(categories_for_full_dataset)
                    # since the number of categories is the same for all the subsets of the same dataset, we only need to get the categories once
                    prev_n_categories.append(len(categories_for_each_dataset))
                    
            
        # save the data for each dataset
        dir_ann = {"images":total_images_for_each,"annotations":total_annotations_for_each,"categories":total_catagories}
        
        with open(os.path.join(source_root,dir,"full_annotations.json"),'w') as file:
            json.dump(dir_ann,file)
            
        full_annotations_for_each[dir] = dir_ann
        

        # save the data for the full dataset
    full_annotations = {"images":total_images,"annotations":total_annotations,"categories":total_catagories}
                
    if not os.path.exists(dest_root):
        os.makedirs(dest_root)
        
    with open(os.path.join(dest_root,"full_annotations.json"),'w') as file:
        json.dump(full_annotations,file)
        
    return full_annotations,full_annotations_for_each
                        

def concat_images(source_root,dest_root):
    
    
    # define the splits
    splits = ["train", "valid", "test"]
    # Get the list of all the images in the main dataset
    dirs = os.listdir(source_root)
    dirs = [os.path.join(source_root, d,split) for d in dirs for split in splits]
    
    # print(dirs)
    
    if not os.path.exists(dest_root):
        os.makedirs(dest_root)
    else:
        answer = input("The destination folder already exists. Do you want to overwrite it? (y/n) ")
        
        if answer == "y":
            shutil.rmtree(dest_root)
            os.makedirs(dest_root)
        
    # Get the list of all the images in the augmented dataset
    for dir in dirs:
        
        images = os.listdir(dir)
        
        for file in images:
            
            if file.split(".")[-1] != "json":

                shutil.copy(os.path.join(dir,file),os.path.join(dest_root,file))
        






if __name__ == "__main__":
    
    root = "../coco_data"
    
    concat_images(root,'source_root')