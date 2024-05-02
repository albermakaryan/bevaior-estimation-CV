from torch.utils.data import Dataset
from torchvision.transforms import Compose, ToTensor, Normalize, Resize, \
        RandomHorizontalFlip, RandomVerticalFlip, RandomRotation
import os
from icecream import ic
import torch
import matplotlib.pyplot as plt
import cv2

# sys.path.append('../helper_functions')


from helper_functions.helper import annotation_extractor



class RCNN_Dataset(Dataset):
    
    
    """
    Custom dataset for RCNN.
    
    """
    
    def __init__(self,image_directory,annotation_file_path,transform=None):
        

        
        """
        Initializes the dataset.
        
        Parameters:
        -----------
        image_directory: str
            Path to the image directory
        annotation_file_path: str
            Path to the annotation file
        transform: torchvision.transforms.Compose
            Transformations to be applied to the images.
            
        
        """
        
        # if os.path.exists(image_directory):
        #     print("Image directory exists.")
        # quit()
        self.image_directory = image_directory
        self.files = [file for file in os.listdir(self.image_directory) if not file.endswith('.json')]
        # self.files = os.listdir(self.image_directory)
        self.annotation_file_path = annotation_file_path
        

        if transform is None:
                self.transform = Compose([ToTensor(),
                                      Resize((224,224)),
                                      RandomHorizontalFlip(0.4),
                                      RandomVerticalFlip(0.4)])
                
                # self.transform = Compose([ToTensor()])

        else:
            
            self.transform = transform
        
        
    def __getitem__(self, index):
        

        """
        Returns the image and the target for the given index, with the given transformations and target format. 
        
        
        Parameters:
        -----------
        index: int
            Index of the image to be returned.
            
        Returns:
        --------
        image: torch.tensor
            Image tensor
        target: dict
            Dictionary containing the target information.
        
        
        """
        
        img = self.files[index]
        file_path = os.path.join(self.image_directory,img)
        

        
        image = plt.imread(file_path) 
        image = cv2.resize(image,(224,224))/255
     
        image.shape = (3,224,224)
        image = torch.as_tensor(image, dtype=torch.float32)
     

        # img = 'pixiz-06-12-2022-14-59-07_jpg.rf.8b6fd4ad3ff4bb6f71e7b070ea6160ff.jpg'
        annotations = annotation_extractor(image_file_name=img,
                                           annotation_file_path=self.annotation_file_path)
                                        
        
        
        old_height,old_width = annotations['height'],annotations['width']
        new_height,new_width = image.shape[1:]
        

        height_ratio = new_height/old_height
        width_ratio = new_width/old_width
        
        bbox = torch.tensor([[bbox[0]*width_ratio,bbox[1]*height_ratio,\
                            (bbox[0]+bbox[2])*width_ratio,(bbox[1]+bbox[3])*height_ratio] for bbox in annotations['bbox']])

       
        
        target = {}
        
        target['labels'] = torch.tensor(annotations['label'])
        
        target['boxes'] = bbox

        
        target['old_height'] = torch.tensor(old_height)
        target['old_width'] = torch.tensor(old_width)
        target['new_height'] = torch.tensor(new_height)
        target['new_width'] = torch.tensor(new_width)

        
        # ic(img)
        # ic(image)
        # ic(target)
        # quit()

        # if target['boxes'].shape == torch.Size([0]):
        #     ic(target)
        #     ic(img)
        #     quit()
        return image,target  


    
    def __len__(self):
        
        """
        Returns the length of the dataset.
        """
        return len(self.files)
    
    
if __name__ == "__main__":
    
    # test if the dataset works properly
    
    ANNOTATION_PATH = "../../DATA/Data_COCO/annotations.coco.json"
    IMAGE_PATH = "../../DATA/Data_COCO/images"

    data = RCNN_Dataset(image_directory=IMAGE_PATH,annotation_file_path=ANNOTATION_PATH)
    
    n = len(data)
    
    for i in range(n):
        print(data[i])
        print("\n\n")
        break
        
    
    ic(n)
