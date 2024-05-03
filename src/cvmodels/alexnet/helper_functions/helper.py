
import json
from icecream import ic
import torch



def get_image_annotations(full_annotations_path,image_id=None,image_file_name=None):
    
    """
    Returns the annotations for the given image id
    
    Parameters
    ----------
    full_annotations_path : str
        path to the full annotations file.
        
    image_id : int
        Image id.
    
    image_file_name : str
        Name of the image file.
        one of image_id or image_file_name should be provided.
        
    Returns
    -------
    list
        list of annotations for the given image id.
    
    """
    
    if image_id is None and image_file_name is None:
        raise ValueError("One of image_id or image_file_name should be provided.")
    
    with open(full_annotations_path,'r') as f:
            
        full_annotations = json.load(f)
        
        annotations = full_annotations['annotations']
        
        if image_id is None:
            
            images = full_annotations['images']
            image_id = [image['id'] for image in images if image['file_name'] == image_file_name][0]
            
        image_annotations = [ann for ann in annotations if ann['image_id'] == image_id]
            

        return image_annotations


def annotation_extractor(image_file_name,
                         annotation_file_path):
    """
    Returns the annotations for the given image file name
    
    Parameters
    ----------
    image_file_name : str
        Name of the image file.
    annotation_file_path : str
        Path to the annotation file.
        
    Returns
    -------
    dict
        Dictionary of annotations.
    
    """
    # open the annotation file
    with open(annotation_file_path,'r') as f:
        
        annotations = json.load(f)
        
           
    # get the image id using image file name
    image = [image for image in annotations['images'] if image['file_name'] == image_file_name][0]
    
    
    image_id = image['id']
    
    # get the annotations for the given image id
    image_annotations = [annotation for annotation in annotations['annotations'] if annotation['image_id'] == image_id]
    
    
    output = dict()
    output['label'] = [annotation['category_id'] for annotation in image_annotations]
    output['bbox'] = [annotation['bbox'] for annotation in image_annotations]
    output['height'],output['width'] = image['height'],image['width']
    

    
    # image_annotation =  {annotation['category_id'] :annotation['bbox'] for annotation in annotations['annotations'] if annotation['image_id'] == image_id}

    
    output['category'] = [category['name'] for id in output['label']for category in annotations['categories'] if category['id'] == id ]
    
    # ic(annotations['categories'])

    
    return output

    
    
if __name__ == "__main__":
    
    # test the function
    
    ANNOTATION_PATH = "../../DATA/Data_COCO/annotations.coco.json"
    IMAGE_PATH = "../../DATA/Data_COCO/images"

    image = '100003_jpg.rf.f52e6e997c347d3ed2feb567faf4a5ef.jpg'
    
    ann = annotation_extractor(image_file_name=image,
                               annotation_file_path=ANNOTATION_PATH)
    
    
    print(ann)
    pass