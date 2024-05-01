
"""
Train the model

"""

if __name__ == "__main__":
    
    from model.model_training import train_model
    
    
    TRAIN_ROOT = "./nnps_coco_format/train"
    VALIDATION_ROOT = "./nnps_coco_format/valid"
    ANNOTAION_PATH = "./nnps_coco_format/balanced_dataset_annotations.json"
    
    train_model(batch_size=1,lerning_rate=0.001,
                epochs=30,mode_save_root='trained_models',
                trainable_backbone_layers=5,
                TRAIN_ROOT = TRAIN_ROOT,
                VALIDATION_ROOT = VALIDATION_ROOT,
                ANNOTAION_PATH = ANNOTAION_PATH)
