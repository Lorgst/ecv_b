import cv2
import numpy as np
import time
import keyboard
from PIL import ImageGrab

#take a screenshot in a defined area
def screen_grab(x,y,w,h):
    img = ImageGrab.grab(bbox=(x,y,w,h)) #x, y, w, h
    img_np = np.array(img)
    return img_np

#load templates to match later
cactus_img = cv2.imread('img\CactusStem.png', cv2.IMREAD_UNCHANGED)
cactus_width = cactus_img.shape[1]
cactus_height = cactus_img.shape[0]
bird_img = cv2.imread('img\Bird.png', cv2.IMREAD_UNCHANGED)
#convert to bw
(thresh, cactus_img) = cv2.threshold(cactus_img, 127, 255, cv2.THRESH_BINARY)
(thresh, bird_img) = cv2.threshold(bird_img, 127, 255, cv2.THRESH_BINARY)

#start loop after return is pressed
keyboard.wait('return')
start_time = time.time()

while True:
    #take a screenshot and save it
    image = screen_grab(190, 550, 1000, 720)
    game_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    #convert to bw and invert if needed
    if game_img[5][745] > 122:
        (thresh, game_img) = cv2.threshold(game_img, 127, 255, cv2.THRESH_BINARY)
    else:
        (thresh, game_img) = cv2.threshold(game_img, 127, 255, cv2.THRESH_BINARY_INV)

    #convert to 8u color depth
    game_img = cv2.cvtColor(game_img, cv2.CV_8U)

    #look for birds and save most likeley position
    bird_result = cv2.matchTemplate(game_img,bird_img, cv2.TM_CCOEFF_NORMED)
    bmin_val, bmax_val, bmin_loc, bmax_loc = cv2.minMaxLoc(bird_result)


    #look for cacti and save possible positions over certain threshold
    result = cv2.matchTemplate(game_img,cactus_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = .6
    ylocs, xlocs = np.where(result >= threshold)

    #group multiple results of the same cactus if at least one cactus was found
    if len(ylocs) > 0:
        cacti = []
        for(x,y) in zip(xlocs, ylocs):
            cacti.append([int(x),int(y),int(cactus_width),int(cactus_height)])
        cacti, weigths = cv2.groupRectangles(cacti, 1, 0.2)

        #then group cacti into clusters
        maxdist = 30
        clusters = [[]]
        prev_x = cacti[0][0]
        i = 0
        for rect in sorted(cacti, key=lambda x: x[0]):
            if (prev_x + maxdist) > rect[0]:
                clusters[i].append(rect)
            else:
                i += 1
                clusters.append([rect])
            prev_x = rect[0]

        #approximate current speed using duration
        duration = time.time() - start_time 
        approx_score = duration/0.11
        speed_bonus = (0.017 * approx_score + 6) / 6

        #jump if catus-cluster is close enugh
        if clusters[0][0][0] <= 250 * speed_bonus:
            keyboard.press('space')
    #jump if bird is close enugh
    if bmax_val >= 0.5:
        if  bmax_loc[0] <= 300 * speed_bonus:
            keyboard.press('space')