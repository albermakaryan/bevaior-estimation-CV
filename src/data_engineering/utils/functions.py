
import json
import numpy as np
import pandas as pd

def get_image_annotations(image_id,annotations):
    
    image_annotations = [ann for ann in annotations if ann['image_id'] == image_id]
    
    return image_annotations


def make_category_annotation_row(annotation,image:dict,scale=True):
    
    
    # bounding box edges
    x,y,w,h = [x for x in annotation['bbox']]
    
    x_centre = (x + (x+w))/2
    y_centre = (y + (y+h))/2
    
    category_id = annotation['category_id']
    # image height and width
    image_height = image['height']
    image_width = image['width']
    
    
    if scale:
        x_centre = x_centre/image_width
        y_centre = y_centre/image_height
        w = w/image_width
        h = h/image_height
        

    return [category_id,x_centre,y_centre,w,h]


def get_label_counts(annotation_file,df=False,numbers=False):

    with open(annotation_file,'r') as file:

        full_annotations = json.load(file)

        annotations = full_annotations['annotations']
        categories = full_annotations['categories']

        id_to_name = {cat['id']:cat['name'] for cat in categories}

        category_counts = [ann['category_id'] for ann in annotations]
        category_counts = np.unique(category_counts,return_counts=True)
        n_categories = len(category_counts[1])
        category_counts = {category_counts[0][i]:category_counts[1][i] for i in range(n_categories)}

        if df:
            category_counts = {id_to_name[key]:[value] for key,value in category_counts.items()}
            category_counts = pd.DataFrame(category_counts).T.reset_index().rename(columns={"index":"Label",0:"Count"})
            category_counts['Proportion'] = round(category_counts['Count']/category_counts['Count'].sum()*100,2)

        else:
            category_counts = {id_to_name[key]:value for key,value in category_counts.items()}

        if numbers:
            return category_counts,id_to_name
        
        return category_counts
    
    


def get_number_of_images_annd_annotationes(annotations_file):
    
    with open(annotations_file,'r') as file:
        
        full_annotations = json.load(file)
        
        images = full_annotations['images']
        annotations = full_annotations['annotations']   
        
        return len(images),len(annotations)
    
    
def get_number_of_multilabels(annotations_file):
    
    with open(annotations_file,'r') as file:
        
        full_annotations = json.load(file)
        
        images = full_annotations['images']
        annotations = full_annotations['annotations']   
        
        
        multilabels = 0
        multilabel_images = []
        
        for image in images:
            
            image_id = image['id']
            image_annotations = get_image_annotations(image_id,annotations)
            
            if len(image_annotations) > 1:
                multilabels += 1
                multilabel_images.append(image)
        
        
        return multilabels,multilabel_images