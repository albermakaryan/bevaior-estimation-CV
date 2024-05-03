from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models import alexnet
from torchvision.models import vgg19
from torch import nn

alexnet(pretrained=True)


from icecream import ic

def alex_net(freeze=False,trainable_backbone_layers=3,number_of_classes=4):

    """
    Returns the model.
    
    Parameters
    ----------
    freeze: bool
        If True, freezes the backbone layers
    trainable_backbone_layers: int
        Number of trainable backbone layers
    number_of_classes: int
        Number of classes
        
    Returns
    -------
    model: torchvision.models.detection.faster_rcnn.FasterRCNN
        Faster RCNN model
    
    """
    
    
    # model = fasterrcnn_resnet50_fpn_v2(weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT)  
    
    # # model = alexnet(pretrained=True)  

    
    # in_feats = model.roi_heads.box_predictor.cls_score.in_features
    # model.roi_heads.box_predictor = FastRCNNPredictor(in_feats,
    #                                                number_of_classes)
    

    # if not freeze:
    #     for name, param in model.named_parameters():
    #         if trainable_backbone_layers > 0 and "backbone" in name:
    #             param.requires_grad = True
    #             trainable_backbone_layers -= 1
    #         else:
    #             param.requires_grad = False

    model = alexnet(pretrained=True)
    # out_features = model.classifier[6].in_features
    model.classifier[6] = nn.Linear(4096, number_of_classes) 

    return model
    
    
    
 