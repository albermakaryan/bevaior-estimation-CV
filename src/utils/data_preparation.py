"""
This file is used to prepare the data for training the model. The functions represted here
are used train, validation and test splits. 
The main problem is that the data is not balanced, and to balance it, the following logic is used:
    -
"""


import json
import os
import numpy as np
import PIL
import cv2


def get_removable_annotations(annotation_path:str,):
    
    
    """
    This function iterates through the annotations list and for each multilable image, it 'removes' some of the annotations. 

    """
    
    
    with open(annotation_path) as f:
        
        full_annotations = json.load(f)
        
        annotations = full_annotations['annotations']
        
        images = full_annotations['images']
        categories = full_annotations['categories']
        
        category_names = [cat['name'] for cat in categories]
        
        n_images = len(images)
        
        annotations_to_remove = []
        
        for i in range(n_images):
            
            image = images[i]
            image_id = image['id']
        
            
            image_annotations = [ann for ann in annotations if ann['image_id'] == image_id and ann['category_id'] != 2] 
            
            
            
            n_annotations = len(image_annotations)
            
            if n_annotations == 1:
                continue
            
            print(categories)
            image_categories = [ann['category_id'] for ann in image_annotations if ann['category_id']  != 2]
            counts = np.unique(image_categories,return_counts=True)

            
            cat_name,cat_count = counts
            blur_counts  = np.ceil((cat_count * cat_count/cat_count.sum())).astype(int)
                        
            blur_count_each_cat = dict(zip(cat_name,blur_counts))
            
            # if there is only one annotation, 
            
            if len(blur_count_each_cat) == 1:
                
                if list(blur_count_each_cat.keys())[0] == 0:
                    blur_count_each_cat[0] = int(blur_count_each_cat[0]/2)
                else:
                    continue
            
            # print(cat_count)
            # print(blur_counts)
            # print(blur_count_each_cat)
            
            # get blure ratio
            
            for ann in image_annotations:
                
                
                removables = list(blur_count_each_cat.values())
                if  np.all(np.array(removables) <= 0):
                    break
                
                print(blur_count_each_cat)
                category_id = ann['category_id']
                print(category_id)
                annotation_id = ann['id']
                
                remove_cat = blur_count_each_cat[category_id]
                
                if remove_cat <=0:
                    continue
                
                annotations_to_remove.append(annotation_id)
                
                if category_id == 0:
                    blur_count_each_cat[category_id] -= .65
                elif category_id == 3:
                    blur_count_each_cat[category_id] -= 2.5
                else:
                    blur_count_each_cat[category_id] -= 1
                    
                
        print(len(annotations_to_remove))            
             
            
        # get new annotations
        new_annotations = [ann for ann in annotations if ann['id'] not in annotations_to_remove]
        new_cat_counts = [ann['category_id'] for ann in new_annotations]
        new_counts = np.unique(new_cat_counts,return_counts=True)
        new_counts = {"cateogory_namge": category_names,
                      "category_id":list(new_counts[0]),
                      "count":list(new_counts[1])}
        # new full annotations
        new_full_annotations = {"annotations":new_annotations,"images":images,"categories":categories}
        
        with open("../data/full_data/balanced_nnps/balanced_dataset_annotations.json","w") as file:
            
            json.dump(new_full_annotations,file)
            
        # save annotations to remove
        with open("../data/full_data/balanced_nnps/annotations_id_to_remove.json","w") as file:
            
            json.dump({'id':annotations_to_remove},file)

            
        
        # # save the counts for each category
        # with open("../data/full_data/balanced_nnps/category_counts.json","w") as file:
            
        #     json.dump(new_counts,file)
  
    
    
    
def blur_images(source_dir='../data/full_data/full_nnps/nnps_full_images',dest_dir='../data/full_data/balanced_nnps/images/'):
    
    
    with open("../data/full_data/full_nnps/nnps_annotations.json",'r') as file_1, \
        open("../data/full_data/balanced_nnps/annotations_id_to_remove.json") as file_2:
            
        full_annotations = json.load(file_1)
        removeables = json.load(file_2)['id']
        
        images = full_annotations['images']
        
        n_images = len(images)
        
        
        for i in range(n_images):
            
            print(f"{'_-_'*20}{i+1}/{n_images}{'_-_'*20}")
            image = images[i]
            image_annotations = [ann for ann in full_annotations['annotations'] if ann['image_id'] == image['id']]
            
            file_name = image['file_name']
            source_path = os.path.join(source_dir,file_name)
            dest_path = os.path.join(dest_dir,file_name)
            
            # print(dest_path)
            # quit()
            
            if os.path.exists(dest_path):
                continue
            
            blured_image = cv2.imread(source_path).copy()
            
            for ann in image_annotations:
                
                if ann['id'] in removeables:
                    
                    x_1, y_1, x_2, y_2 = [int(x) for x in ann['bbox']]
                    
                    blur_y, blur_height = y_1, y_2
                    blur_x, blur_width = x_1, x_2
                    roi = blured_image[blur_y:blur_y + blur_height, blur_x:blur_x + blur_width]
                    blur_image = cv2.GaussianBlur(roi, (911, 911), 0)
                    blured_image[blur_y:blur_y + blur_height, blur_x:blur_x + blur_width] = blur_image

                    

            cv2.imwrite(dest_path,blured_image)
            # quit()
        # print(len(removeables))
        
        
    
    
if __name__ == "__main__":
    
    # annotation_path = "../data/full_data/full_nnps/nnps_annotations.json"
    # get_removable_annotations(annotation_path)
    
    blur_images()