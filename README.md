## Project Structure

- **[src/](./src/)**: source code and data

    - **[cvmodels/](./src/cvmodels/)**
        - **[yolov8/](https://github.com/WongKinYiu/yolov7)**: Yolo version 7. Model is to large, so it is not pushed. You can check it go to the link provided.

        - **[rcnn/](./src/cvmodels/rcnn/)** : R-CNN.

           - **[helper_functions/](./src/cvmodels/rcnn/helper_functions/)**: Function used to prepare data.
                - **[collate.py](./src/cvmodels/rcnn/helper_functions/collate.py)**: Function to collate batch before giving to model as an input.
                - **[helper.py](./src/cvmodels/rcnn/helper_functions/helper.py)** : Functions to get image annotations in the model input format.
                - **[split_roots.py](./src/cvmodels/rcnn/helper_functions/split_roots.py)**: Function to split data into train, test, and validation sets.
                - **[visual.py](./src/cvmodels/rcnn/helper_functions/visual.py)**: Function to plot images with annotations.

           - **[model/](./src/cvmodels/rcnn/model/)**: Files containing functions to train R-CNN.
                - **[__init__.py](./src/cvmodels/rcnn/model/__init__.py)**: Package initializer.
                - **[dataset.py](./src/cvmodels/rcnn/model/dataset.py)** : A custom Dataset object (inherited torch Dataset).
                - **[model_training.py](./src/cvmodels/rcnn/model/model_training.py)**: The main function for model training.
                - **[predict.py](./src/cvmodels/rcnn/model/predict.py)** : Function for prediction.
                - **[train.py](./src/cvmodels/rcnn/model/train.py)** : Functions for model training.
                - **[validate.py](./src/cvmodels/rcnn/model/validate.py)** : Function to evaluate model performance.

           - **[main.py](./src/cvmodels/rcnn/main.py)** : The main function where model is training.

        
    - **[data_engineering/](./src/data_engineering/)**

        - **[utils/](./src/data_engineering/utils/)**: Utility functions for data engineering.
        - **[data_engineering_results.ipynb](./src/data_engineering/data_engineering_results.ipynb)**: Steps of data preparation with visualizations.
        - **[dem_reduction.ipynb](./src/data_engineering/dem_reduction.ipynb)**: Examples of dimensionality reduction
        - **[]()**
    