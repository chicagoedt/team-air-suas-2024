# Text detection

**1. Setup Requirement**

  Install the following libraries: opencv-python (for computer vision), easyocr (text-detection pre-trained model)


        pip3 install opencv-python
        pip3 install easyocr

**2. Where to begin**

  The main file in this folder is textDetection.py

  ![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/c82f9c2f-aac4-4352-9855-532d80ae9455)

  Put a folder path of the input image in folderPath. Put its name inside imgName_list. 

  ![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/b161546c-f547-4f8d-b34c-e784fc9494a0)

  For example in here we have img_024__tar_001.jpg which is number 7. We can use its relative path: /img_024_tar_001.jpg.

  - Put the path of the folder that stores this image in folderPath (in this case an empty string).

  - Put the name of image in imageName_list (in this case "img_024_tar_001.jpg")

  Try to run the code and see the result. If you just install easyocr then what happens is that it will first download 
  
  the easyocr model to your local machine (which takes time). But later as your machine already has easyocr then it will

  not go through that downloading step.

  ![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/05add462-a9a4-4d6a-af0a-8a554b3940be)

  The output that we get is in the second list, which is '7'
