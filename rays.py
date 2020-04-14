import pygame 
import numpy as np
from math import pi , cos, sin
from random import randint

#var
width = 700
height = 700
res = (width, height)
white = (255,255,255)
red = (255,0,0)

class Ray:
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        pygame.draw.aaline(window, red, [x1,y1],[x2,y2])


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
        pygame.draw.aaline(window,red,(self.x1,self.y1),pt)

class Wall:
    walls = []
    bigWalls = [[0,0,width,0],
                [0,0,0,height],
                [0,height,width,height],
                [width,0,width,height]]
    def __init__(self,x1,y1,x2,y2):
        #graph
        pygame.draw.aaline(window, white, [x1,y1],[x2,y2])
        #calc
        Wall.walls.append([x1,y1,x2,y2])
    
    def draw():
        for wall in Wall.walls:
            pygame.draw.aaline(window, white, (wall[0],wall[1]), (wall[2], wall[3]))

    def create_walls(N):
        for i in range(N):
            newwall = Wall(randint(0,width),randint(0,height),randint(0,width),randint(0,height))

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
window = pygame.display.set_mode(res)
launched = True
Wall.create_walls(5)

while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
    pygame.display.flip()
    pos = pygame.mouse.get_pos()
    newParticle = Particle(pos[0],pos[1],201)
    pygame.draw.rect(window,(0,0,0),pygame.Rect(0,0,width,height))
    Wall.draw()
    newParticle.cast()








