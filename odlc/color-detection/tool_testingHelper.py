import random
import itertools

# choose num random images from images_list, return a list of the chosen images
def chooseRandomImages(images_list, num):
    randomImages_list = []
    idx_used = []
    for i in range(num):
        idx = random.randint(0, len(images_list) - 1)
        if idx in idx_used:
            idx = random.randint(0, len(images_list) - 1)
        image = images_list[idx]
        randomImages_list.append(image)
    return randomImages_list

# given a list, shuffle it in the list and return the shuffled list
def shuffleList(sth_list):
    permutations_list = list(itertools.permutations(sth_list))
    idx = random.randint(0, len(permutations_list) - 1)
    return permutations_list[idx]