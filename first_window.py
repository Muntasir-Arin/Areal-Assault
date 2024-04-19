import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 1280, 720
def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

#---------------------------------------------- Mid-Point Line Drawing Algorithm
def plot_point(x, y, point_size):
    glPointSize(point_size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glFlush()

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def midpoint_line(x1, y1, x2, y2, point_size):
    dx = x2 - x1
    dy = y2 - y1

    # Determine the zone
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    # Convert to zone 0
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)

    dx = x2 - x1
    dy = y2 - y1

    # calculate initial decision parameter
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)

    # plot initial point
    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    plot_point(x0, y0, point_size)
    

    # iterate over x coordinates
    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        # Convert back from zone 0
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0, point_size)

#------------------------------------------------------------------Mid-Point Circle Drawing Algorithm
        

def midpointcircle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2*x - 2*y + 5
            y -= 1
        x += 1
    glEnd()


#-----------------------------------------------------------------------------------
    
def draw_square(x, y, length, width):
    point_size = 3
    midpoint_line(x,y,x+width, y, point_size)
    midpoint_line(x,y,x, y-length, point_size)
    midpoint_line(x,y-length,x+width, y-length, point_size)
    midpoint_line(x+width,y-length,x+width, y, point_size)

def draw_heart(x,y):
    point_size = 4
    midpoint_line(x+0*point_size,y+0*point_size,x+0*point_size,y-8*point_size, point_size)
    midpoint_line(x+1*point_size,y+1*point_size,x+1*point_size,y-7*point_size, point_size)
    midpoint_line(x+2*point_size,y+2*point_size,x+2*point_size,y-6*point_size, point_size)
    midpoint_line(x+3*point_size,y+2*point_size,x+3*point_size,y-5*point_size, point_size)
    midpoint_line(x+4*point_size,y+1*point_size,x+4*point_size,y-4*point_size, point_size)
    midpoint_line(x+5*point_size,y+0*point_size,x+5*point_size,y-3*point_size, point_size)

    midpoint_line(x-1*point_size,y+1*point_size,x-1*point_size,y-7*point_size, point_size)
    midpoint_line(x-2*point_size,y+2*point_size,x-2*point_size,y-6*point_size, point_size)
    midpoint_line(x-3*point_size,y+2*point_size,x-3*point_size,y-5*point_size, point_size)
    midpoint_line(x-4*point_size,y+1*point_size,x-4*point_size,y-4*point_size, point_size)
    midpoint_line(x-5*point_size,y,x-5*point_size,y-3*point_size, point_size)

def draw_a(x,y,letter_size):
    midpoint_line(x+0*letter_size,y-1*letter_size, x+0*letter_size, y-4*letter_size, letter_size)
    midpoint_line(x+4*letter_size,y-1*letter_size, x+4*letter_size, y-4*letter_size, letter_size)
    midpoint_line(x+1*letter_size,y+0*letter_size, x+3*letter_size, y+0*letter_size, letter_size)
    midpoint_line(x+1*letter_size,y-3*letter_size, x+3*letter_size, y-3*letter_size, letter_size)

def draw_r(x,y,letter_size):
    midpoint_line(x+0*letter_size,y+0*letter_size, x+3*letter_size, y+0*letter_size, letter_size)
    midpoint_line(x+0*letter_size,y+0*letter_size, x+0*letter_size, y-4*letter_size, letter_size)
    midpoint_line(x+4*letter_size,y-1*letter_size, x+4*letter_size, y-2*letter_size, letter_size)
    midpoint_line(x+4*letter_size,y-4*letter_size, x+4*letter_size, y-4*letter_size, letter_size)
    midpoint_line(x+0*letter_size,y-3*letter_size, x+3*letter_size, y-3*letter_size, letter_size)

def draw_e(x,y,letter_size):
    midpoint_line(x+0*letter_size,y+0*letter_size, x+4*letter_size, y+0*letter_size, letter_size)
    midpoint_line(x+0*letter_size,y+0*letter_size, x+0*letter_size, y-4*letter_size, letter_size)
    midpoint_line(x+0*letter_size,y-2*letter_size, x+3*letter_size, y-2*letter_size, letter_size)
    midpoint_line(x+0*letter_size,y-4*letter_size, x+4*letter_size, y-4*letter_size, letter_size)

def draw_l(x,y,letter_size):
    midpoint_line(x+0*letter_size,y+0*letter_size, x+0*letter_size, y-3*letter_size, letter_size)
    midpoint_line(x+1*letter_size,y-4*letter_size, x+4*letter_size, y-4*letter_size, letter_size)

def draw_s(x,y,letter_size):
    midpoint_line(x+0*letter_size,y+0*letter_size, x+3*letter_size, y+0*letter_size, letter_size)
    midpoint_line(x-1*letter_size,y-1*letter_size, x-1*letter_size, y-1*letter_size, letter_size)
    midpoint_line(x+0*letter_size,y-2*letter_size, x+2*letter_size, y-2*letter_size, letter_size)
    midpoint_line(x+3*letter_size,y-3*letter_size, x+3*letter_size, y-3*letter_size, letter_size)
    midpoint_line(x-1*letter_size,y-4*letter_size, x+2*letter_size, y-4*letter_size, letter_size)

def draw_u(x,y,letter_size):
    midpoint_line(x+0*letter_size,y+0*letter_size, x+0*letter_size, y-3*letter_size, letter_size)
    midpoint_line(x+4*letter_size,y+0*letter_size, x+4*letter_size, y-3*letter_size, letter_size)
    midpoint_line(x+1*letter_size,y-4*letter_size, x+3*letter_size, y-4*letter_size, letter_size)

def draw_t(x,y,letter_size):
    midpoint_line(x+0*letter_size,y+0*letter_size, x+4*letter_size, y-0*letter_size, letter_size)
    midpoint_line(x+2*letter_size,y+0*letter_size, x+2*letter_size, y-4*letter_size, letter_size)


def display_first_screen():

    # glPointSize(2)
    glColor3f(0,0,255)
    midpoint_line(-640,360,640,360,2)
    midpoint_line(-640,-360,640,-360,2)
    midpoint_line(-640,-360,-640,360,2)
    midpoint_line(640,-360,640,360,2)
    midpoint_line(640,-360,640,360,2)
  
    x = -640
    y = 360
    
    draw_square(x+210, y - 55, 95, 155)
    draw_square(x+915, y - 55, 95, 155)

    draw_square(x+210, y - 190, 350, 860)
    
    draw_square(x+210, y - 605,60,370)
    draw_square(x+700, y - 605,60,370)

    # start button
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    draw_square(x+505, y - 425,60,270)
    letter_size = 3
    glColor3f(255, 255, 0)#yellow
    draw_s(x+606, y-450, letter_size)
    draw_t(x+622, y-450, letter_size)
    draw_a(x+640, y-450, letter_size)
    draw_r(x+658, y-450, letter_size)
    draw_t(x+676, y-450, letter_size)
    
    draw_heart(x+310,y-560)#4
    draw_heart(x+900,y-560)#6

    glColor3f(255, 182, 193)
    
    glColor3f(255, 0, 0)#red
    draw_heart(x+288,y-90)#7
    
    draw_heart(x+380,y-560)#5
    glColor3f(1,.27,0)#orange
    draw_heart(x+970,y-560)#2
    draw_heart(x+993,y-90)#8

    glColor3f(.93,.5,.93)#violet
    draw_heart(x+1040,y-560)#1
    draw_heart(x+240,y-560)#3
    letter_size = 9
    draw_a(x+505,y-270,letter_size)
    draw_r(x+560,y-270,letter_size)
    draw_e(x+615,y-270,letter_size)
    draw_a(x+670,y-270,letter_size)
    draw_l(x+725,y-270,letter_size)

    draw_a(x+450,y-330,letter_size)
    draw_s(x+515,y-330,letter_size)
    draw_s(x+570,y-330,letter_size)
    draw_a(x+615,y-330,letter_size)
    draw_u(x+670,y-330,letter_size)
    draw_l(x+725,y-330,letter_size)
    draw_t(x+780,y-330,letter_size)

    
    
    glColor3f(1,1,.1)
    
    # plot_point(x+454, y-572, 7)
    p = 440
    for i in range(30):
        plot_point(x+p, y-572, 7)
        p = p + 14
    
    t = 605
    for i in range(5):
        plot_point(x+639, y-t, 7)
        t = t + 14


  

