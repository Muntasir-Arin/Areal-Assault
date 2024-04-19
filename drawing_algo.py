import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from math import sin, cos, pi



#<<<<<<<<-----------------------------------Mohammed Saalem --------------------------------------------->>>>>>>>
#<<<<<<<<-----------------------------------Mohammed Saalem --------------------------------------------->>>>>>>>
#<<<<<<<<-----------------------------------Mohammed Saalem --------------------------------------------->>>>>>>>
border=[] #list of all points to draw for the borders
bg=None

frame=0
#file


W_Width, W_Height = 1280, 720
def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    glFlush()
#-----------------------------------drawing algorithms-------------------------------------------

#----------midpoint circle algo
def circlepoints(x, y, a,b, zone=""):
    #list that contains all the points for each zone 0-8
    l=[(x+a,y+b),(y+a,x+b),(y+a,-x+b),(x+a,-y+b),(-x+a,-y+b), (-y+a,-x+b), (-y+a,x+b), (-x+a,y+b)] 

    if zone:#checks if zone numbers were mentioned
        out=[]
        for i in zone:
            out.append(l[i])
        
        return out #returns a list of tuples containing only the points in the specified zones

    else:
        return l #returns a list of tuples for all zones


def midpointcircledraw(x1,y1,r, *zone): #call function to get list of points
    """Returns a list of points to draw a line from two given points"""
    # x1, y1= p[0], p[1]
    points=[] #store all the points to draw after reverting in format=> points=[(x,y), (x,y).....]
    x=0
    y=r
    d=1-r

    
    #plotting the points
    while x<y:
        if d>=0: #choose SE
            d+=2*x - 2*y + 5
            x+=1
            y-=1


            points.extend(circlepoints(x,y,x1,y1, zone))
            

        else: #choose E
            d+=2*x + 3
            x+=1
            
            points.extend(circlepoints(x,y,x1,y1, zone))


    return points #returns list of points


#----------midpoint line algo

#midpoint line algo
def fz(x1, y1, x2, y2): #findzone function

    dx=x2 - x1
    dy=y2 - y1
    # z=None #zone

    if abs(dy)>abs(dx):
        #z 1 2 5 6 
        if dy>0:
            if dx>0:
                z=1
            else:
                z=2       
        else:
            if dx>0:
                z=6
            else:
                z=5

    else: #|dx| > |dy|
        #z 0 3 4 7
        if dy>0:
            if dx>0:
                z=0
            else:
                z=3       
        else:
            if dx>0:
                z=7
            else:
                z=4

    return z

def convert(x, y, z):
    if z==0:
        pass
    if z==1:
        x,y = y,x
    if z==2:
        x,y = y,-x
    if z==3:
        x,y = -x,y
    if z==4:
        x,y = -x,-y
    if z==5:
        x,y = -y,-x
    if z==6:
        x,y = -y,x
    if z==7:
        x,y = x,-y

    return x,y,z #returns a tuple

def revert(x,y,z):
    if z==0:
        pass
    if z==1:
        x,y = y,x
    if z==2:
        x,y = -y,x
    if z==3:
        x,y = -x,y
    if z==4:
        x,y = -x,-y
    if z==5:
        x,y = -y,-x
    if z==6:
        x,y = y,-x
    if z==7:
        x,y = x,-y

    return x,y #returns a tuple

dp = {}
def midpointlinedraw(x1,y1,x2,y2): #call function to get list of points
    global dp
    temp = f'{x1}{y1}{x2}{y2}'
    if temp in dp:
        return dp[temp]
    """Returns a list of points to draw a line from two given points"""
    # x1, y1, x2, y2= p[0], p[1], p[2], p[3]
    points=[(x1,y1)] #store all the points to draw after reverting in format=> item=[(x,y), (x,y).....]
    
    #calculating zones and converting start adn end points
    z=fz(x1, y1, x2, y2)
    s=convert(x1, y1, z)
    e=convert(x2, y2, z)

    #finding dx and dy using converted points
    dx=e[0] - s[0]
    dy=e[1] - s[1]

    #calculating the increments
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    
    #initializing the function
    d=2*dy-dx
    x=s[0]
    y=s[1]
    
    #plotting the points
    while x<e[0]:
        if d>0: #choose NE
            d+=incrNE
            x+=1
            y+=1

            points.append(revert(x,y,z)) #appends points to the list

        else: #choose E
            d+=incrE
            x+=1
            
            points.append(revert(x,y,z)) #appends points to the list

    dp[temp] = points
    return points #returns list of points

def fill(point:list, red, green, blue, dir=-1):
    if dir==-1: #fill under the line to border
        for idx in range(0, len(point), 50):
            i = point[idx]
            temp=midpointlinedraw(i[0], i[1], i[0], -358)
            glPointSize(70)
            drawpoints(temp, red, green, blue)

    else:
        for idx in range(0, len(point), 50):
            i = point[idx]
            temp=midpointlinedraw(i[0], i[1], i[0], 358)
            glPointSize(70)
            drawpoints(temp, red, green, blue)

brokenline_dp={}
def brokenline(points:list):
    global brokenline_dp
    z = ','.join([f"({point[0]},{point[1]})" for point in points])
    if z in brokenline_dp:
        return brokenline_dp[z]
    if z in brokenline_dp:
        return brokenline_dp[z]
    output=[]
    for i in range(0, len(points)-1):
        output.extend(midpointlinedraw(points[i][0], points[i][1], points[i+1][0], points[i+1][1]))
    brokenline_dp[z]=output
    return output

#---------draw function

def drawpoints(points:list, red, green, blue):
    """Draws points in the given list with the colors"""
    glBegin(GL_POINTS)
    glColor3f(red/255, green/255, blue/255)#color
    for i in points:
        glVertex2f(i[0],i[1])
    glEnd()


#<<<<<<<<-----------------------------------Mohammed Saalem --------------------------------------------->>>>>>>>
#<<<<<<<<-----------------------------------Mohammed Saalem --------------------------------------------->>>>>>>>
#<<<<<<<<-----------------------------------Mohammed Saalem --------------------------------------------->>>>>>>>







#<<<<<<<<-----------------------------------Mahim Muntasir---------------------------------------------->>>>>>>>
#<<<<<<<<-----------------------------------Mahim Muntasir---------------------------------------------->>>>>>>>
#<<<<<<<<-----------------------------------Mahim Muntasir---------------------------------------------->>>>>>>>

#---------------------------------------------- Mid-Point Line Drawing Algorithm




#<<<<<<<<-----------------------------------Mahim Muntasir---------------------------------------------->>>>>>>>
#<<<<<<<<-----------------------------------Mahim Muntasir---------------------------------------------->>>>>>>>
#<<<<<<<<-----------------------------------Mahim Muntasir---------------------------------------------->>>>>>>>
