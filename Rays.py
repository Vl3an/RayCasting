import pygame 
import numpy as np
from math import pi , cos, sin
from random import randint

#var
#width = 500
#height = 500
width = 1920 
height = 1080
res = (width, height)
white = (255,255,255)
red = (250,250,250)
speed = 100
rayNumber = 255
auto = True
x = int(width /2)
y = int(height /2) 
xspeed = 5
yspeed = 5
speedlimit = 5
timer = 0


class Color:
    counter = 0
    def __init__(self):
        self.value = [randint(0,255),randint(0,255),randint(0,255)]

    def modify(self):
        Color.counter += 1
        if Color.counter == speed:
            self.value[0] += randint(-1,1)
            self.value[1] += randint(-1,1)
            self.value[2] += randint(-1,1) 
            for i in range(3):
                if self.value[i] > 255:
                    self.value[i] = 255
                elif self.value[i] < 0:
                    self.value[i] = 0
            Color.counter = 0
            

class Ray:

    color = Color()

    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def cast(self):
        for bwall in Wall.bigWalls:
            x3 = bwall[0]
            x4 = bwall[2]
            y3 = bwall[1]
            y4 = bwall[3]
            A = (self.x1 - self.x2)*(y3 - y4) - (self.y1 - self.y2)*(x3- x4)
            if A != 0:
                t = ((self.x1 - x3)*(y3 - y4) - (self.y1 - y3)*(x3- x4))/A
                u = -((self.x1 - self.x2)*(self.y1 - y3) - (self.y1 - self.y2)*(self.x1- x3))/A
                if 0 <= t and u >= 0 and u <= 1:
                    pt = ((self.x2-self.x1) * t + self.x1, (y4-y3)*u + y3)
                    break
        for wall in Wall.walls:
            x3 = wall[0]
            x4 = wall[2]
            y3 = wall[1]
            y4 = wall[3]
            A = (self.x1 - self.x2)*(y3 - y4) - (self.y1 - self.y2)*(x3- x4)
            if A != 0:
                t = ((self.x1 - x3)*(y3 - y4) - (self.y1 - y3)*(x3- x4))/A
                u = -((self.x1 - self.x2)*(self.y1 - y3) - (self.y1 - self.y2)*(self.x1- x3))/A
                if 0 <= t and u >= 0 and u <= 1:
                    newPt = ((self.x2-self.x1) * t + self.x1, (y4-y3)*u + y3)
                    if abs(newPt[0] - self.x1) < abs(pt[0]- self.x1):
                        pt = newPt
        Ray.color.modify()
        pygame.draw.aaline(window,Ray.color.value,(self.x1,self.y1),pt)

class Wall:
    walls = []
    bigWalls = [[-1,-1,width+1,-1],
                [-1,-1,-1,height+1],
                [-1,height+1,width+1,height+1],
                [width+1,-1,width+1,height+1]]
    def __init__(self,x1,y1,x2,y2):
        #graph
        pygame.draw.aaline(window, white, [x1,y1],[x2,y2])
        #calc
        Wall.walls.append([x1,y1,x2,y2])
    
    def draw():
        for wall in Wall.walls:
            pygame.draw.aaline(window, white, (wall[0],wall[1]), (wall[2], wall[3]))

    def create_alea_walls(N):
        for i in range(N):
            newWall = Wall(randint(0,width),randint(0,height),randint(0,width),randint(0,height))
        
    def create_walls():
        creating = True
        while creating:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        creating = False
                    elif event.key == pygame.K_p:
                        point = 0
                        placed = False
                        draw = False
                        while (not placed) or (point < 2): 
                            for event in pygame.event.get():
                                if draw:
                                    pygame.draw.rect(window,(0,0,0),pygame.Rect(0,0,width,height))
                                    Wall.draw() 
                                    pygame.draw.line(window,(100,100,100),pos_1,pygame.mouse.get_pos())
                                    pygame.display.flip()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    point += 1 
                                    if point == 1:
                                        pos_1 = pygame.mouse.get_pos()
                                        draw = True
                                    elif point == 2:
                                        pos_2 = pygame.mouse.get_pos()
                                        newWall =  Wall(pos_1[0],pos_1[1],pos_2[0],pos_2[1])
                                        Wall.draw() 
                                        placed = True
                                        pygame.display.flip()
    def delete():
        Wall.walls = []


class Particle:
    def __init__(self,x,y,N):
        self.rays = []
        self.pt = (x,y)
        #N = int(abs(N + (N==0))) #N entier strictement positif
        for i in range(1,N+1):
            newRay = Ray(x,y,x + 5*cos(i/N * 2* pi),y + 5*sin(i/N * 2 * pi))    
            self.rays.append(newRay)

    def cast(self):
        for ray in self.rays:
            ray.cast()



pygame.init()
print("Pour placer un mur pressez 'P', puis cliquez pour le placer , un fois les murs placés ; appuyez sur échap pour lancer.")
a = input("tapez pour lancer : ")

window = pygame.display.set_mode(res)
pygame.display.set_mode(res,pygame.FULLSCREEN)
launched = True
Wall.create_alea_walls(10)

while launched:
    timer += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
    pygame.display.flip()
    if not auto:
        pos = pygame.mouse.get_pos()
        newParticle = Particle(pos[0],pos[1],rayNumber)
    else:
        xspeed += randint(-1,1) - (xspeed > speedlimit) + (xspeed < -speedlimit)
        yspeed += randint(-1,1) - (yspeed > speedlimit) + (yspeed < -speedlimit)
        x += xspeed
        y += yspeed
        x = x - xspeed*((x > width) + (x < 0))
        y = y - yspeed*((y > height) + (y < 0))

        newParticle = Particle(x,y,rayNumber)
        #
        #pos = pygame.mouse.get_pos()
        #newParticle_2 = Particle(pos[0],pos[1],rayNumber)
        #
    if timer >= 500:
        timer = 0
        Wall.delete()
        Wall.create_alea_walls(randint(2,10))
    pygame.draw.rect(window,(0,0,0),pygame.Rect(0,0,width,height))
    Wall.draw()
    newParticle.cast()
    #newParticle_2.cast()








