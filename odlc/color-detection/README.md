# Color detection

**1. Setup Requirement**

install these libraries: opencv-python, numpy

    pip3 install opencv-python
    pip3 install numpy   

**2. Where to begin**

  **Main file**: colorDetection.py

  You can start with colorDetection.py which detects the shape color and letter color of a target.

  Let say we want to pass the img_020_tar_001.jpg

![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/0f7dae13-df01-4aae-a98a-e9d655689999)

Its relative path is /img_020_tar_001.jpg. So you may set the values for folderPath and imgName_list as follow:

![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/5feb16c0-0dc0-43ec-8a37-d57d5627bb2e)

It should get the shape color be blue and letter color be red like in the image below:

![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/aa286d51-8f03-48e5-a17e-1fb18f61dfb6)


# Locating target using color

**1. Setup Requirement**

  Install packages: opencv-python, numpy

    pip3 install opencv-python
    pip3 install numpy

**2. Where to begin**

Main file: targetLocate.py

![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/96d017c0-12f4-4ac8-a66d-1fc36a82bf07)


Let say we want to find the target in the above image (or you can refer to image img_023_tar_000.jpg located in this folder).

First, pass the path of image (/img_023_tar_000.jpg) to folderPath and imgName_list like below. In here folderPath is the path

of the folder that stores image (here it is empty string) and imgName_list is a list that stores string of name of image

(here it is "img_023_tar_000.jpg"). 

![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/661bc506-4c9a-4b30-9ad8-ed301e37ac0c)


Run the code. You should see something like below:

![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/a57b5c5a-ef19-44b3-ae2a-f61079025663)

There are two lists here and they both have meaning:

- ['Brown', (3207, 2658), 54]: There is a brown target located at coordinate (3207, 2658) and its size is around 54 * 54px

- ['Orange', (3729, 2358), 93]: There is an orange target located at coordinate (3729, 2358) and its size is around 93 * 93px


If you check the folder cropImages, there will be two images generated after you run this code. They are cropped from the 

large input image. Notice that the algorithm correctly finds the orange target and incorrectly identify a brown target.

That is an issue that need to be resolved.

![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/c877f727-6690-4e09-a829-152d85a82caf)     ![image](https://github.com/chicagoedt/team-air-suas-2024/assets/92337557/926fbce4-10d9-43c9-869e-c9f01f5fae14)

