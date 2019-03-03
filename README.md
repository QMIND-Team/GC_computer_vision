# GC_computer_vision
##    Intro    ##
Main repo for the Grocery Checkout Team's computer vision project


##    Setup    ##

The data in this file is used in combination with the TF models file found here:
https://github.com/tensorflow/models

1. Replace the protos file found at models\research\object_detection\Protos with the proto file found in this git. (Ignore this step if you have already set up tensorflow)
2. Move the vision_app.py file and model('ssd_resnet50' folder) to models\research\object_detection
3. Install the required packages using pip install -r requirements.txt, consider a virtual environment for this
4. run the vision_app.py file using terminal, a video screen will pop up if setup was done correctly


### Creating a venv ###
to use this project you need a venv outside of this project directory.
create one with virutalenv venv
activate it with . venv/bin/activate
deactivate it with deactivate
when you want tp update the requirements.txt for everyone use pip freeze > requirements.txt (must be in the project directory)

### Common Matplot Issue ###
to change matplotlib backend 
cd ~/.matplotlib
touch maplotlibrc
emacs matplotlibrc
backend: TkAgg 

## Setup ##
Consider using a virtual environment for this project using:
``` 
virutalenv venv
```
Activate your venv using:
```
. venv/bin/activate
```
1. Install tensorflow
```
# For CPU
pip install tensorflow
# For GPU
pip install tensorflow-gpu
```
2. Install additional libraries
```
pip install --user Cython
pip install --user contextlib2
pip install --user pillow
pip install --user lxml
pip install --user jupyter
pip install --user matplotlib
```
3. Additionally, install any other required libraries using form the requirements.txt file using:
```
pip install -r requirements.txt
```

4. Clone tensorflow/models git: https://github.com/tensorflow/models
```
git clone https://github.com/tensorflow/models.git
```
5. Download the latest protobuf compiler from: https://github.com/protocolbuffers/protobuf/releases
6. Unzip the protoc and tensorflow/models-master files, and rename models-master to just models. You should have the following folders:
   - bin
   - include
   - models
7. Protobuf compilation:
```
# From tensorflow/models/research/
protoc object_detection/protos/*.proto --python_out=.
```
8. When running locally, the tensorflow/models/research/ and slim directories should be appended to PYTHONPATH. This can be done by running the following from tensorflow/models/research/:
```
# From tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
Note: This command needs to run from every new terminal you start. If you wish to avoid running this manually, you can add it as a new line to the end of your ~/.bashrc file, replacing `pwd` with the absolute path of tensorflow/models/research on your system.

9. To test your installation:
```
# from models/research/
python object_detection/builders/model_builder_test.py
```
