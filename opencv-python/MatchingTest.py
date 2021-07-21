import cv2
import numpy as np
#load all needed images
game_img = cv2.imread('img\MatchTest.png', cv2.IMREAD_UNCHANGED)
cactus_img = cv2.imread('img\CactusStem.png', cv2.IMREAD_UNCHANGED)
bird_img = cv2.imread('img\Bird.png', cv2.IMREAD_UNCHANGED)

#display them and away a key
cv2.imshow('Game', game_img)
cv2.waitKey()
cv2.destroyAllWindows()

cv2.imshow('Cactus', cactus_img)
cv2.waitKey()
cv2.destroyAllWindows()

cv2.imshow('Vogel', bird_img)
cv2.waitKey()
cv2.destroyAllWindows()

#locate most likely positions of the bird and draw a light blue rectangle around it
bird_result = cv2.matchTemplate(game_img,bird_img, cv2.TM_CCOEFF_NORMED)
bmin_val, bmax_val, bmin_loc, bmax_loc = cv2.minMaxLoc(bird_result)
bird_width = bird_img.shape[1]
bird_height = bird_img.shape[0]
cv2.rectangle(game_img,bmax_loc,(bmax_loc[0]+bird_width,bmax_loc[1] + bird_height),(255,122,0),2)
#print the bird's location
print("Bird Location x:",bmax_loc[0]+bird_width/2,", y:",bmax_loc[1] + bird_height/2)
#show how closely every location matches the template
cv2.imshow('Result Vogel', bird_result)
cv2.waitKey()
cv2.destroyAllWindows()

#locate most likely positions of cacti
result = cv2.matchTemplate(game_img,cactus_img, cv2.TM_CCOEFF_NORMED)
#show how closely every location matches the template
cv2.imshow('Result', result)
cv2.waitKey()
cv2.destroyAllWindows()

#only keep the location above threshold
threshold = .6
ylocs, xlocs = np.where(result >= threshold)

#draw dark blue rectangles at every remaining position
cactus_width = cactus_img.shape[1]
cactus_height = cactus_img.shape[0]
for(x,y) in zip(xlocs, ylocs):
    cv2.rectangle(game_img,(x,y),(x + cactus_width, y + cactus_height),(255,0,0),2)

#group overlapping rectangles
if len(xlocs)>0:
    rects = []
    for(x,y) in zip(xlocs, ylocs):
        rects.append([int(x),int(y),int(cactus_width),int(cactus_height)])
    xmax = max(xlocs)
    ymax = max(ylocs)

    xmin = min(xlocs)
    ymin = min(ylocs)

    rects, weigths = cv2.groupRectangles(rects, 1, 0.2)
    #and draw them in green
    for(x,y,w,h) in rects:
        cv2.rectangle(game_img,(x,y),(x + w, y + h),(0,255,0),2)

    #print information about all cacti
    print("Cactus: x, y, w, h")
    for(x) in sorted(rects, key=lambda x: x[0]):
        print(x)

    #group cacti into clusters
    maxdist = 30
    clusters = [[]]
    prev_x = rects[0][0]
    i = 0
    for rect in sorted(rects, key=lambda x: x[0]):
        if (prev_x + maxdist) > rect[0]:
            clusters[i].append(rect)
        else:
            i += 1
            clusters.append([rect])
        prev_x = rect[0]

    #print start of each cluster
    print("x-start of clusters:")
    for cluster in clusters:
        print(cluster[0][0])
    #draw red rectangles around all clusters
    for cluster in clusters:
        cv2.rectangle(game_img,(cluster[0][0],cluster[0][1]),(cluster[len(cluster)-1][0] + cactus_width,cluster[len(cluster)-1][1] + cactus_height),(0,0,255),2)

cv2.imshow('Game', game_img)
cv2.waitKey()
cv2.destroyAllWindows()