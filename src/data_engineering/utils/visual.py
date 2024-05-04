import matplotlib.pyplot as plt
import os
import json
from utils.functions import get_image_annotations
import cv2

from copy import deepcopy
import numpy as np

def get_annotated_image(original_image,annotationes,categories,
                           font = cv2.FONT_HERSHEY_SIMPLEX,
                           font_scale = 1,
                           color = (255, 0, 0),
                           thickness = 2):

    image = original_image.copy()
    
    for img_ann in annotationes:
        
        x_1,y_1,x_2,y_2 = [int(x) for x in img_ann['bbox']]
        x_1,y_1 = x_1,y_1
        x_2,y_2 = x_2,y_2
        cat_id = img_ann['category_id']
        cat_name = [cat['name'] for cat in categories if cat['id'] == cat_id][0]
    
        cv2.rectangle(image,(x_1,y_1),(x_1+x_2,y_1+y_2),(0,255,0),2)
        cv2.putText(image, cat_name, (x_1,y_1+20), font, font_scale, color, thickness)
        
    return image




def plot_image_with_annotations_comparison(image_root_new,image_root_old,annotations_file_balanced,annotations_file_original,number_of_iamges=8,shuffle=False):


    with open(annotations_file_balanced,"r") as file_new, open(annotations_file_original,'r') as file_orig:

        balanced_annotations_full = json.load(file_new)
        original_annotations_full = json.load(file_orig)
        
            

        images = deepcopy(balanced_annotations_full['images'])
        
        if shuffle:
            np.random.shuffle(images)
            
        categories = balanced_annotations_full['categories']

        new_annotationes = balanced_annotations_full['annotations']
        old_annotationes = original_annotations_full['annotations']

        # construct a subplot

        cols = 2
        rows = number_of_iamges

        fig,ax = plt.subplots(rows,cols)

        fig.set_figheight(30)
        fig.set_figwidth(20)

        # iterate
        j = 50

        for i in range(number_of_iamges):

            # get those which are multilabeled

            while True:
                
                image = images[j]
                image_id = image['id']
                
                image_file = image['file_name']
                new_image_annotations = get_image_annotations(image_id,new_annotationes)
                old_image_annotations = get_image_annotations(image_id,old_annotationes)
                n_annotationes = len(new_image_annotations)
                j += 1
                
                # print(len(old_image_annotationes))
                if n_annotationes > 1:
                    break


            old_image = plt.imread(os.path.join(image_root_old,image_file)).copy()
            new_image = plt.imread(os.path.join(image_root_new,image_file)).copy()

            # old annotationes
            old_image = get_annotated_image(old_image,old_image_annotations,categories)
            # new annotationes
            new_image = get_annotated_image(new_image,new_image_annotations,categories)
            
            ax[i][0].imshow(old_image)
            ax[i][0].set_title("Old image")
            ax[i][0].axis("off")

            ax[i][1].imshow(new_image)
            ax[i][1].set_title("New image")        
            ax[i][1].axis("off")
        plt.show()


        
    



def plot_image_with_annotations(image_root,annotations_file,images_files=None,number_of_iamges=8,multilabel=False):


    with open(annotations_file,"r") as file:

        annotations_full = json.load(file)

        images = annotations_full['images']
        
        if images_files is not None:
            images = [img for img in images if img['file_name'] in images_files]
            number_of_iamges = len(images)
            
        categories = annotations_full['categories']

        annotationes = annotations_full['annotations']

        # construct a subplot

        cols = 2
        rows = int(number_of_iamges/2)

        fig,ax = plt.subplots(rows,cols)

        fig.set_figheight(30)
        fig.set_figwidth(20)
        axes = ax.flatten()

        # iterate
        j = 0
        for i in range(number_of_iamges):

            # get those which are multilabeled

            while True:
                
                image = images[j]
                image_id = image['id']
                
                image_file = image['file_name']
                image_annotations = get_image_annotations(image_id,annotationes)
                n_annotationes = len(image_annotations)
                j += 1
                
                # print(len(old_image_annotationes))
                if n_annotationes > 1 or not multilabel:
                    break


            orig_image = plt.imread(os.path.join(image_root,image_file)).copy()

            # old annotationes
            orig_image = get_annotated_image(orig_image,image_annotations,categories)
            # new annotationes
            
            axes[i].imshow(orig_image)
            axes[i].set_title(f"Image {i+1} with annotationes")
            

        plt.show()


        
    pass
    


def plot_label_counts(counts,title=None):


    title = 'Counts of labels' if title is None else title
    
    n_lables = len(counts.Label)
    max_count = counts.Count.max()  


    plt.figure(figsize=(10,7))
    plt.bar(counts['Label'],counts['Count'])
    

    for i,value in enumerate(counts.Count):
        
        percent = counts.Proportion.values[i]
        
        text =  f"{str(value)}\n[{percent}%]"
        
        plt.text(i, value, text, ha='center', va='bottom')

    if n_lables > 7:
        plt.xticks(rotation=45)
        
    add_lim = max_count * 0.15
    
    plt.ylim(0,max_count+add_lim)
        
    plt.xlabel("Emotion")
    plt.ylabel("Count")
    plt.title(title)
    plt.show()
    
