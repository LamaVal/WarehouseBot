import cv2 as cv
import numpy as np


def Distance(x1,y1,x2,y2):
    x = x1-x2
    y = y1-y2
    return ((x)**2+(y)**2)


def FNode():
    img = cv.imread("cci.png")
    blank = np.zeros(img.shape,"uint8")
#    grey = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    blur = cv.GaussianBlur(img,(5,5),cv.BORDER_DEFAULT)
    canny = cv.Canny(blur,120,230)
    contours,heir = cv.findContours(canny,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)

    rcontours = []#for storing points of approx points
    for i in contours:
        epi = 0.01*cv.arcLength(i,1)
    
        refined = cv.approxPolyDP(i,epi,1)
        for j in refined:
            if(j[0,1] <62 or j[0,1]>1025):
                break

        else:
            rcontours.append(refined) #contour poins added only if the they are in a certain range i.e. above eryc logo
            
    del(blur)
    del(canny)
    del(contours)
    del(heir)


    
    for i in range(len(rcontours)):                    #filtering the duplicate rows
        rcontours[i] = np.unique(rcontours[i],axis = 0)
    i = 0
    j = len(rcontours)-1
    while i<j:                     
        if np.array_equal(rcontours[i],rcontours[i+1]): #filtering duplicate contours
            rcontours.pop(i+1)
            j-=1
        else:
            i+=1


    onlyPoints = [] #list unique points // ease to access
    for i in range(len(rcontours)):
        for j in range(rcontours[i].shape[0]):
            onlyPoints.append(rcontours[i][j,0])
    del rcontours

    
    PosNode = [] 
    PosNode.append([[onlyPoints[0].item(0),onlyPoints[0].item(1)]]) #entire thing to cluster the nodes
    for i in range(len(onlyPoints)):
        for j in range(len(PosNode)):
            x1 = onlyPoints[i].item(0)
            y1 = onlyPoints[i].item(1)
            x2 = PosNode[j][0][0]
            y2 = PosNode[j][0][1]
            if( Distance(x1,y1,x2,y2)<7000):           #if point is in certain distance range it put with the any cluster     
                PosNode[j].append([x1,y1])
                break
        else:
            PosNode.append([[x1,y1]])                   #here the point is away from all cluster hence it will start new cluster

    del onlyPoints


    FinalNodes = np.zeros((len(PosNode),2),int)     #array for saving average of coordinates of the clusters
    for i in range(len(PosNode)):
        for j in range(len(PosNode[i])):            
            FinalNodes[i][0]+= PosNode[i][j][0]     #summation of x coordinates
            FinalNodes[i][1]+= PosNode[i][j][1]     #summation of y coordinates
        FinalNodes[i][0]//= len(PosNode[i])         #divison by total entries
        FinalNodes[i][1]//= len(PosNode[i])
   
    del PosNode
    for i in FinalNodes:                            #plotting circles on the main image
        cv.circle(img,i,30,(255,255,255),-1)
    
        #print(i)

    blur = cv.GaussianBlur(img,(5,5),cv.BORDER_DEFAULT)
    canny = cv.Canny(blur,120,230)
    contours,heir = cv.findContours(canny,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    rcontours = []
    for i in contours:
        epi = 0.01*cv.arcLength(i,1)
    
        refined = cv.approxPolyDP(i,epi,1)
        for j in refined:
            if(j[0,1] <62 or j[0,1]>1025):
                break
        else:
            rcontours.append(refined)
    
    
    #check for refined points of the lines
    #check if any of the nodes are in 900 radius then it is connected. 


    cv.imshow("pointOnBlank",img)
    cv.waitKey(0)

    

FNode()
