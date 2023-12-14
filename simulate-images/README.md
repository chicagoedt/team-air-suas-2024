# SIMULATING IMAGES

**1. Setup Requirements**

   - install the following libraries: Pillow, shapely (these libraries are used for dealing with images)
  
   - You can install them with PIP (a Python package management):
  
         pip3 install Pillow shapely

**2. How to use it**

  - your main file will be gen_train_images.py. Run that file:
    
    ![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/7f0404d9-5e54-4158-aa9e-aa3ec2119b16)

    There is a confusing question about "snapshot". Basically, "snapshot" is an empty image (a part of runaway without

    target on it) and they will be stored in /simulate-images/snapshots/no-target folder. Now input the number you want

    , say 1. Then you are done now, the simulated images are generated. You can find the simulated images in

    /simulate-images/snapshots/target/


    ![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/e8adf1c5-582b-439b-a201-470d1febf015)

    You will also see in the folder snapshots there is a csv file named "target_info" which keep tracks of the information

    about the target in each generated image. In the folder target there are not only images but also a bunch of file with

    extension YOLO. These files can be helpful for training YOLO model in case we intend to use it.
