# GC_computer_vision
##    Intro    ##
Main repo for the Grocery Checkout Team's computer vision project


##    SETUP    ##

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