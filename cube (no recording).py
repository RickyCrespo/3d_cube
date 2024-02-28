# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:41:25 2024

@author: rcres
"""

# -*- coding: utf-8 -*-
import pyglet
import numpy as np
import math as m
from pyglet import app
from pyglet import clock
from pyglet import shapes
from pyglet.window import key
from pyglet.gl import Config
from pyglet.window import Window


config = Config(sample_buffers=1, samples=8, double_buffer=True)
window = Window(828,1792, config=config) #828,1792
pyglet.gl.glClearColor(1,1,1,1)
batch = pyglet.graphics.Batch()
#window.set_fullscreen(True)
framerate = 120

#Function deorator (añade la función de abajo al Window)
@window.event
def on_draw():
    #Clear todo
    window.clear()
    batch.draw()

def update(dt):
    #Modulators!
    global angle1, angle2, angle3, a, b, c, dir1 ,dir2, dir3
    if not pause:
        if angle1 >= 4 * m.pi:
            angle1 = 0
        if a == 255:
            dir1 = -1
        elif a == 0:
            dir1 = 1
        if b == 255:
            dir2 = -1
        elif b == 0:
            dir2 = 1
        if c == 255:
            dir3 = -1
        elif c == 0:
            dir3 = 1
        
        angle1 += (m.pi/6)/framerate
        angle2 += 1/(5 * m.pi) * (m.sin(angle1))
        a += dir1
        b += dir2
        c += dir3
    
    #Rotation matrices
    x_rotation = np.matrix([
                        [1, 0, 0],
                        [0, m.cos(angle1), -m.sin(angle1)],
                        [0, m.sin(angle1), m.cos(angle1)]
                    ])

    y_rotation = np.matrix([
                        [m.cos(angle2), 0, m.sin(angle2)],
                        [0, 1, 0],
                        [-m.sin(angle2), 0, m.cos(angle2)]
                    ])

    z_rotation = np.matrix([
                        [m.cos(angle3), -m.sin(angle3), 0],
                        [m.sin(angle3), m.cos(angle3), 0],
                        [0, 0, 1]
                    ])
    
    #Projections and rotations
    for i in range(8):
        rotated = np.dot(x_rotation, vertices[i].reshape((3,1)))
        rotated = np.dot(y_rotation, rotated)
        #rotated = np.dot(z_rotation, rotated)
        projected[i] = np.dot(projection, rotated)
        #dots[i] = shapes.Circle((scale * projected[i][0,0]) + X_OFFSET, (scale * projected[i][1,0]) + Y_OFFSET, 3, color=(50, 225, 30), batch=batch)

    i2 = 0
    i3 = 1
    for i1 in range(len(lines)):
    
        if i1 == 3:
            i2 += 1
            i3 += 1
        elif i1 == 6:
            i2 = 0
            i3 = 4
        elif i1 == 10:
            i2 = 0
            i3 = 3
        elif i1 == 11:
            i2 = 4
            i3 = 7
        
        lines[i1] = shapes.Line((scale * projected[i2][0,0]) + X_OFFSET, (scale * projected[i2][1,0]) + Y_OFFSET, 
                            (scale * projected[i3][0,0]) + X_OFFSET, (scale * projected[i3][1,0]) + Y_OFFSET,
                            width=2, color=(a, b, c), batch=batch)
        i2 += 1
        i3 += 1


@window.event
def on_key_press(symbol, modifiers):
    global pause
    
    if pause:
        pause = False
        return
    
    if symbol == key.P:
        pause = True
    

#Variables
X_OFFSET = int(window.width/2) + 1
Y_OFFSET = int(window.height/2) + 1
angle1 = angle2 = angle3 = 0
a = 37
b = 116
c = 243
dir1 = dir2 = 1
dir3 = -1
dots = [0] * 8
projected = [0] * 8
lines = [0] * 12
scale = 50
pause = False
frame = 0

#Matrices
projection = np.matrix([
                    [1, 0, 0],
                    [0, 1, 0],
                ])

vertices = []
vertices.append(np.matrix([-1, -1, 1]))
vertices.append(np.matrix([1, -1, 1]))
vertices.append(np.matrix([1, 1, 1]))
vertices.append(np.matrix([-1, 1, 1]))
vertices.append(np.matrix([-1, -1, -1]))
vertices.append(np.matrix([1, -1, -1]))
vertices.append(np.matrix([1, 1, -1]))
vertices.append(np.matrix([-1, 1, -1]))

#Framerate 30
clock.schedule_interval(update,1/framerate)

#Start app
app.run()