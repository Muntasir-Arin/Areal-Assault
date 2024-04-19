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

def draw_box(x,y):
    point_size = 3
    draw_square(x,y,120,120)
    midpoint_line(x,y,x+60,y+60,point_size)
    midpoint_line(x,y,x+60,y+60,point_size)
    midpoint_line(x+60, y+60, x+180, y+60,point_size)
    midpoint_line(x+120, y-120, x, y-120,point_size)
    midpoint_line(x+180,y+60,x+180,y-60,point_size)
    plot_point(x+60,y-60,120)
   
    t=0
    for i in range(40):
        midpoint_line(x+120,y+t, x+180, y+60+t,point_size)
        t = t - 3
    midpoint_line(x+120, y-120, x+180, y-60,point_size)

def draw_arrow(x,y):
    x1=x
    y1=y
    x2=x
    y2=y
    point_size = 5
    t = 1

    for i in range(40):
        midpoint_line(x1-t,y1+t,x2-t,y2-t,point_size)
        t = t + 1

def draw_arrow_above_box(x,y):
    x1=x
    y1=y
    x2=x
    y2=y
    point_size = 5
    t = 1

    for i in range(40):
        midpoint_line(x1-t,y1+t,x2+t,y2+t,point_size)
        t = t + 1

def display_box(box_choose):

    # glPointSize(2)
    glColor3f(0,0,255)
    midpoint_line(-640,360,640,360,2)
    midpoint_line(-640,-360,640,-360,2)
    midpoint_line(-640,-360,-640,360,2)
    midpoint_line(640,-360,640,360,2)
    midpoint_line(640,-360,640,360,2)
  
    x = -640
    y = 360
    
    draw_square(x+150,y-90,540,1075)

    glColor3f(.93,.5,.93)#violet
    draw_heart(x+90,y-590)
    draw_heart(x+90,y-450)

    glColor3f(1,.27,0)#orange
    draw_heart(x+90,y-520)
    draw_heart(x+90,y-380)

    glColor3f(255, 255, 0)#yellow
    t = 95
    for i in range(12):
        plot_point(x+90, y-t, 10)
        t = t + 20

    glColor3f(.83, .73, .53)#box color
    draw_box(x+280,y-400)
    draw_box(x+610,y-400)
    draw_box(x+940,y-400)
    
    glColor3f(1,1,1)
    draw_arrow(x+1225,y-630)
    draw_arrow(x+1190,y-630)

    if box_choose == 1:
        draw_arrow_above_box(x+370,y-250)
        draw_arrow_above_box(x+370,y-285)

    elif box_choose == 2:
        draw_arrow_above_box(x+700,y-250)
        draw_arrow_above_box(x+700,y-285)
    else :
        draw_arrow_above_box(x+1030,y-250)
        draw_arrow_above_box(x+1030,y-285)

