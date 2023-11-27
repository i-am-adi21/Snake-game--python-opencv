
import math
import cv2
import random
import cvzone
import numpy as np
class SnakeGameClass:
    def __init__(self,pathFood):
        self.initializeData()
        self.gameOver=False
        self.score=0
        self.imgFood=cv2.imread(pathFood,cv2.IMREAD_UNCHANGED)
        self.hFood,self.wFood , _ =self.imgFood.shape 
        
    def randomLocation(self):
        self.foodPoint=random.randint(100,300),random.randint(100,300)
    def initializeData(self):
        self.points=[] 
        self.lenghts=[]
        self.currentLength=0
        self.allowedLength=150
        self.previousHead=0,0
        self.foodPoint=0,0
        self.randomLocation()
        
        
        
    def update(self,imgMain,currentHead):
        
        if self.gameOver:
            cvzone.putTextRect(imgMain,"Game Over",[300//2,400//2],scale=3,thickness=3,
                            offset=20)
            cvzone.putTextRect(imgMain,f'Your Score {self.score}',[300//2,550//2],scale=3,thickness=3,
                            offset=20)
            
        else:
            cx,cy=currentHead
            px,py=self.previousHead
            self.points.append((cx,cy))
            distance= math.hypot(cx-px,cy-py)
            self.lenghts.append(distance)
            self.currentLength+=distance
            self.previousHead=cx,cy
            self.reduceLength()
            rx,ry=self.foodPoint
            if(rx-self.wFood//2 <cx<rx+self.wFood//2 and ry-self.hFood//2
               <cy<ry+self.hFood//2):
                self.score+=1
                
                self.allowedLength+=50
                self.randomLocation()
            
            #draw snake
            if(self.points):
                for i,point in enumerate(self.points):
                    if i!=0:
                        cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),15)
                cv2.circle(imgMain,self.points[-1],15,(200,0,200),cv2.FILLED)
            
            #draw count
            cvzone.putTextRect(imgMain,f'Score {self.score}',[50,80],scale=3,thickness=2,
                                offset=10)
            imgMain=cvzone.overlayPNG(imgMain,self.imgFood, (rx-self.wFood//2,ry-self.hFood//2))
            
            #check for collision
            pts=np.array(self.points[:-2],np.int32)
            pts=pts.reshape((-1,1,2))
            cv2.polylines(imgMain,[pts],False,(0,200,0),2)
            distace=cv2.pointPolygonTest(pts,(cx,cy),True)
            if(-1<=distace<=1):
                self.gameOver=True
                self.initializeData()
               
        return imgMain
                
    def reduceLength(self)  :
        if(self.currentLength>self.allowedLength):
            for i, lenght in enumerate(self.lenghts):
                self.currentLength-=lenght
                self.lenghts.pop(i)
                self.points.pop(i)
                if(self.currentLength < self.allowedLength):
                    break
          
                
            
        
        
        
