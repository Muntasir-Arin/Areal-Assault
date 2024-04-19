import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from math import sin, cos, pi
from scene import *
import time
import math

W_Width, W_Height = 1280, 720
launched = False
current_scene = 4
round = 1

# Constants
initial_velocity = 65 # Initial velocity of the projectile
gravity = 4  # Acceleration due to gravity (m/s^2)
time_step = 1 # Time step for simulation
velocity_x=0
velocity_y=0
class Ball :
    def __init__(self):
        self.x = -501
        self.y = -259
        self.r = 20
        self.color = [random.uniform(0.3, 1.0) for _ in range(3)]
        self.angle=0
    def reset(self):
        self.x = -501
        self.y = -259
        self.angle=0
        self.color = [random.uniform(0.3, 1.0) for _ in range(3)]

ball= Ball()


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

def midpoint_line(x1, y1, x2, y2):
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
    plot_point(x0, y0)
    

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
        plot_point(x0, y0)

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

def draw_heart(color, middle_point):
    # Convert color string to RGB values
    if color == "sky blue":
        glColor3f(0.529, 0.808, 0.922)  # Sky blue
    elif color == "red":
        glColor3f(1.0, 0.0, 0.0)  # Red
    elif color == "pink":
        glColor3f(1.0, 0.753, 0.796)  # Pink

    # Set middle point
    x, y = middle_point

    # Draw heart shape using points
    glPointSize(2)
    glBegin(GL_POINTS)
    

    for t in range(0, 360, 1):
        theta = t * pi / 180.0
        x_heart = 16 * (sin(theta) ** 3)
        y_heart = 13 * cos(theta) - 5 * cos(2 * theta) - 2 * cos(3 * theta) - cos(4 * theta)

        glVertex2f(x + x_heart, y + y_heart)

    glEnd()

def draw_ball():
    global ball
    glPointSize(3)
    glColor3f(ball.color[0], ball.color[1], ball.color[2])
    midpointcircle(ball.r, ball.x, ball.y)

def find_angle(x, y):
    global ball,velocity_x, velocity_y
    # Define the coordinates of the fixed point
    fixed_x = -501
    fixed_y = -259
    
    # Calculate the differences in x and y coordinates
    delta_x = x - fixed_x
    delta_y = y - fixed_y
    
    # Calculate the angle using arctan2
    angle = math.atan2(delta_y, delta_x) * 180 / math.pi
    
    # Ensure the angle is between 0 and 360 degrees
    # if angle < 0:
    #     angle += 360
    
    ball.angle= min(angle+20,90)

    velocity_x = initial_velocity * math.cos(math.radians(ball.angle))
    velocity_y = initial_velocity * math.sin(math.radians(ball.angle))

def draw_chest(x,y):
    x1=x-60
    x2=x+60
    y1=y-5
    y2=y+5
    glColor3f(0.851, 0.529, 0)  
    glPointSize(10)
    midpoint_line(x1, y1, x2, y1)
    midpoint_line(x1, y2, x2, y2)
    midpoint_line(x1, y2, x1, y1)
    midpoint_line(x2, y2, x2, y1)

    y1-=50
    y2-=25
    glColor3f(1, 0.773, 0.4)
    glPointSize(10)
    midpoint_line(x1, y1, x2, y1)
    midpoint_line(x1, y2, x2, y2)
    midpoint_line(x1, y2, x1, y1)
    midpoint_line(x2, y2, x2, y1)

    y1+=10
    y2-=10
    glColor3f(1, 0.839, 0.573)
    glPointSize(10)
    midpoint_line(x1, y1, x2, y1)
    midpoint_line(x1, y2, x2, y2)
    midpoint_line(x1, y2, x1, y1)
    midpoint_line(x2, y2, x2, y1)



def draw_box(x1,y1,x2,y2, w):
    glColor3f(0.0, 0.0, 1.0)  # Border color (blue)
    glPointSize(w)
    midpoint_line(x1, y1, x2, y1)
    midpoint_line(x1, y2, x2, y2)
    midpoint_line(x1, y2, x1, y1)
    midpoint_line(x2, y2, x2, y1)


def draw_barrel(x1,y1,x2,y2):
    glColor3f(0.2784, 0.1765, 0.0196)
    glPointSize(50)
    midpoint_line(x1, y1, x2, y2)
    glPointSize(40)
    glColor3f(0.3184, 0.2165, 0.116)

    midpoint_line(x1, y1, x2, y2)

    glPointSize(30)
    glColor3f(0.3584, 0.2565, 0.156)

    midpoint_line(x1, y1, x2, y2)
    glPointSize(10)

    glColor3f(0.3884, 0.2965, 0.216)
    midpoint_line(x1, y1, x2, y2)

def draw_cannon():
    global launched
    glColor3f(0.30, 0.2804, 0.3863)
    if launched:
        glColor3f(0.10, 0.1804, 0.1863)
    glPointSize(18)
    midpointcircle(35, -470,-250)

    glColor3f(0.9720, 0.6804, 0.0863)
    glPointSize(20)
    midpointcircle(45, -500,-265)
    glColor3f(0.9420, 0.604, 0.0863)
    glPointSize(20)
    midpointcircle(25, -500,-265)
    glColor3f(0.8412, 0.4706, 0.0588)
    glPointSize(11)
    midpointcircle(8, -500,-265)
    


#-----------------------------------------------------------------------------------
def scene0():  #
    draw_ball()
    draw_cannon()
    



def start_screen():
    # Set text color
    glColor3f(1.0, 1.0, 1.0)  # Text color (white)

    # Scale the bitmap font
    glPushMatrix()
    glRasterPos2f(-125, 30)  # Position of the text (adjusted)
    glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, b"AREAL")
    glRasterPos2f(-125, 0)  # Position of the text (adjusted)
    glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, b"ASSAULT")
    glColor3f(1.0, 0.5, 0.796)
    glRasterPos2f(-50, -170) 
    glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, b"START!")
    glPopMatrix()  # Restore the original scale

    # Set color for border (blue)
    draw_box(500,250,-500,-250, 7)
    draw_box(550,275,-550,-275, 7)
    draw_box(140,-140,-140,-185, 5)
    draw_heart("sky blue", (0, 0))
    draw_heart("red", (50, 50))
    draw_heart("pink", (-50, -50))
    pass
    


def round_screen():
    global round
    glColor3f(1.0, 1.0, 1.0)  # Text color (white)

    # Scale the bitmap font
    glPushMatrix()

    glColor3f(1.0, 0.5, 0.796)
    glRasterPos2f(-50, -10) 
    round_string = "ROUND " + str(round)
    round_bytes = round_string.encode('utf-8')
    glutBitmapString(GLUT_BITMAP_TIMES_ROMAN_24, round_bytes)
    glPopMatrix()  # Restore the original scale

    # Set color for border (blue)

    draw_box(550,275,-550,-275, 7)

    pass


def box_screen():
    # Scene 3 code here
    pass

def canon_screen():
    background_dessert()
    draw_ball()
    draw_cannon()
    draw_chest(40,-250)
    draw_chest(240,-250)
    draw_chest(440,-250)

def hit_miss_screen(flag):
    # Scene 3 code here
    pass

def win_screen():
    # Scene 3 code here
    pass
#-----------------------------------------------------------------------------------
def animate():
    global current_scene, round, angle, ball,initial_velocity,launched, velocity_x,velocity_y
    # current_time = time.time()
    # delta_time = current_time - animate.start_time if hasattr(animate, 'start_time') else 0
    # animate.start_time = current_time

    if current_scene==2:
        time.sleep(1)
        current_scene+=1
    if current_scene==4:
        if launched:
            ball.x += velocity_x * time_step
            ball.y += velocity_y * time_step - 0.3 * gravity * time_step**2
            velocity_y -= gravity * time_step
            if ball.y <= -350 or ball.x >= 630 or ball.y >= 355:
                ball.reset()
                launched= False


    # time.sleep(1/60)
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global current_scene,launched
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        print(c_x, c_y)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if current_scene== 1:
            if -140 < c_x < 140 and -185 < c_y < -140:
                current_scene=2
        if current_scene== 4:
            c_x, c_y = convert_coordinate(x, y)
            if not launched:
                find_angle(c_x, c_y)
                launched=True
                
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        pass

    glutPostRedisplay()
#-----------------------------------------------------------------------------------

def display():
     #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0);	#//color black
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    #//now give three info
    #//1. where is the camera (viewer)?
    #//2. where is the camera looking?
    #//3. Which direction is the camera's UP direction?
    gluLookAt(0,0,314,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    if current_scene == 0:
        scene0()
    elif current_scene == 1:
        start_screen()
    elif current_scene == 2:
        round_screen()
    elif current_scene == 3:
        box_screen()
    elif current_scene == 4:
        canon_screen()

    glutSwapBuffers()
    
def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(98, (1280/720), 1, 1000.0)
    # **(important)**aspect ratio that determines the field of view in the X direction (horizontally). The bigger this angle is, the more you can see of the world - but at the same time, the objects you can see will become smaller.
    #//near distance
    #//far distance

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color


# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Game")
init()

glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is occuring)
glutMouseFunc(mouseListener)
# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)

glutMainLoop()		#The main loop of OpenGL






