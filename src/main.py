from utils.concat import concat_images,concat_annotations
from utils.resplit import resplit_by_label

if __name__ == "__main__":
    
    root = "./coco_data"
    
    split = False
    
    if split:
        concat_annotations(root,'./full_data/')
        concat_images(root,'./full_data/full_images/')
    resplit_by_label("./full_data/full_images/","./full_data/full_annotations.json","./full_data/splitted_by_label/")
   