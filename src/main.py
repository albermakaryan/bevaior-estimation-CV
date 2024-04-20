from utils.concat import concat_images,concat_annotations
from utils.resplit import resplit_by_label, resplit_by_nnps,resplit_sets_by_nnps
from cvmodels.yolov7 import detect

if __name__ == "__main__":
    
    root = "./data/coco_data"
    
    split = False
    
    if split:
        
        # concat all annotations from all sources to one file
        concat_annotations(root,'./data/full_data/')
        
        # collect all images from all sources to one folder
        concat_images(root,'./data/full_data/full_images/')
        
        # resplit the data by label
        resplit_by_label("./data/full_data/full_images/","./data/full_data/full_annotations.json","./data/full_data/splitted_by_label/")
        
        # combine the labels with the nnps [Negative, Positive, Natural, Surprise]
        resplit_by_nnps("./data/full_data/full_images","./data/full_data/full_annotations.json","./data/full_data/full_nnps")
        
    root = "./data/full_data/full_nnps/nnps_full_images"
    ann_path = "./data/full_data/full_nnps/nnps_annotations.json"
    
    
    resplit_sets_by_nnps(root,ann_path,'')
    