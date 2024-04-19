import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from math import sin, cos, pi



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




def background_dessert():
   
    #setting up the sky
    point=midpointlinedraw(-638, 358, 638, 358)
    drawpoints(point, 201,93,65)    
    fill(point, 201,93,65, -1) 

    #drawign the sun
    sun=midpointcircledraw(0,-60, 350)
    drawpoints(sun, 252,72,94)
    fill(sun, 255,15,47, -1)

    #mountain layers
    line=[(-638,166),(-574,190),(-516,175),(-477,205),(-406,173),(-376,142),(-359,155),(-337,172),(-307,193),(-265,182),(-257,161),(-237,138),(-209,117),(-190,137),(-168,158),(-126,178),(-96,193),(-52,210),(-27,206),(22,194),(49,185),(81,179),(118,172),(154,172),(186,169),(214,180),(236,188),(255,197),(273,210),(287,219),(298,229),(315,233),(330,227),(362,216),(388,210),(414,202),(425,199),(446,205),(461,213),(474,219),(488,227),(504,224),(511,213),(519,205),(533,196),(548,193),(561,201),(566,214),(578,229),(586,245),(590,259),(602,256),(610,242),(619,226),(638,209)]
    points=brokenline(line)
    drawpoints(points, 203,50,70)
    fill(points, 203,50,70, -1)

    line=[(-638,195),(-559,153),(-522,156),(-500,170),(-473,186),(-458,192),(-438,203),(-409,218),(-304,79),(-252,109),(-236,66),(-225,51),(-214,47),(-196,43),(-180,39),(-158,49),(-142,77),(-123,112),(-102,144),(-67,166),(-46,181),(-22,152),(10,112),(55,78),(101,53),(145,37),(182,30),(209,64),(236,87),(266,105),(275,118),(292,111),(314,90),(347,69),(374,98),(420,65),(443,26),(457,34),(460,57),(462,88),(482,118),(509,130),(535,84),(557,49),(572,94),(583,65),(590,115),(605,144),(615,125),(638,109)]
    points=brokenline(line)
    drawpoints(points, 179, 34, 53)
    fill(points, 179, 34, 53, -1)

    line=[(-638,-143),(-616,-137),(-591,-131),(-583,-127),(-558,-119),(-536,-112),(-525,-110),(-511,-109),(-476,-105),(-466,-105),(-438,-105),(-424,-108),(-410,-115),(-399,-122),(-364,-141),(-342,-148),(-319,-153),(-310,-152),(-286,-145),(-278,-138),(-263,-130),(-250,-124),(-221,-116),(-216,-113),(-205,-108),(-188,-100),(-157,-91),(-146,-87),(-143,-87),(-128,-88),(-101,-100),(-96,-105),(-86,-115),(-64,-129),(-34,-140),(-12,-154),(7,-161),(62,-177),(69,-179),(94,-186),(120,-193),(143,-199),(159,-203),(182,-207),(201,-212),(220,-216),(240,-217),(261,-208),(279,-201),(287,-199),(308,-192),(321,-185),(355,-179),(366,-174),(372,-172),(392,-162),(407,-158),(411,-160),(426,-175),(439,-193),(457,-211),(460,-209),(480,-196),(499,-185),(510,-176),(520,-165),(526,-156),(535,-148),(547,-134),(554,-128),(560,-126),(573,-137),(577,-142),(587,-154),(601,-175),(605,-182),(638,-203)] 
    points=brokenline(line)
    drawpoints(points, 145, 17, 34)
    fill(points, 145, 17, 34, -1)
    

    #footing
    line=[(-633,-249),(-609,-244),(-584,-238),(-545,-233),(-515,-226),(-502,-226),(-472,-228),(-458,-228),(-393,-231),(-366,-235),(-339,-237),(-323,-237),(-301,-237),(-263,-244),(-235,-244),(-186,-249),(-164,-249),(-137,-241),(-110,-231),(-94,-224),(-76,-217),(-55,-209),(-45,-205),(-35,-205),(-16,-213),(2,-217),(28,-221),(47,-225),(84,-229),(115,-231),(139,-232),(159,-232),(197,-231),(217,-227),(234,-224),(249,-223),(270,-219),(298,-217),(335,-216),(360,-216),(377,-216),(412,-220),(429,-222),(455,-223),(480,-223),(499,-222),(525,-217),(574,-210),(585,-210),(594,-210),(602,-210),(613,-213),(619,-215),(625,-219)]
    points=brokenline(line)
    drawpoints(points, 43, 2, 7)
    fill(points, 43, 2, 7, -1)



def background_night():

    #setting up the sky
    point=midpointlinedraw(-638, 358, 638, 358)
    drawpoints(point, 1,1,1)    
    fill(point, 1,1,1, -1) 


    line=[(-622,110),(-581,125),(-525,142),(-494,154),(-482,160),(-460,170),(-418,185),(-393,194),(-374,201),(-336,214),(-312,219),(-286,220),(-251,220),(-241,220),(-215,205),(-193,196),(-179,191),(-157,183),(-122,167),(-113,162),(-93,151),(-67,141),(-44,138),(-24,136),(21,136),(35,139),(75,145),(100,156),(119,163),(154,172),(181,180),(222,192),(257,201),(288,207),(321,214),(349,220),(387,229),(409,237),(435,243),(459,250),(487,259),(515,264),(527,266),(542,267),(570,258),(579,253),(595,244),(611,237),(621,232),(625,230),(626,229)]
    points=brokenline(line)
    drawpoints(points, 9, 8, 59)
    fill(points, 9, 8, 59, -1)
    
    line=[(-627,-107),(-604,-84),(-580,-37),(-556,-17),(-548,-4),(-526,22),(-505,46),(-487,61),(-471,64),(-441,40),(-429,34),(-413,31),(-396,23),(-374,16),(-345,12),(-316,9),(-295,8),(-267,15),(-256,20),(-244,29),(-233,38),(-221,49),(-209,59),(-192,70),(-173,80),(-163,83),(-154,83),(-138,82),(-126,80),(-122,79),(-101,65),(-93,60),(-74,60),(-60,62),(-43,69),(-26,78),(-14,87),(15,131),(20,140),(40,160),(57,181),(75,203),(90,213),(106,219),(130,230),(159,233),(183,223),(208,206),(219,197),(247,174),(256,167),(272,156),(289,146),(313,136),(324,131),(362,112),(378,106),(403,101),(458,99),(484,97),(495,94),(510,83),(519,70),(526,57),(539,31),(543,20),(547,9),(551,3),(564,-14),(573,-26),(582,-37),(590,-45),(604,-55),(611,-60),(621,-66),(623,-68),(626,-70),(627,-70)]
    points=brokenline(line)
    drawpoints(points, 3, 2, 46)
    fill(points, 3, 2, 46 -1)
    
    line=[(-638,-178),(-613,-167),(-603,-158),(-589,-140),(-573,-122),(-559,-106),(-538,-92),(-524,-79),(-511,-68),(-500,-63),(-483,-61),(-472,-61),(-455,-62),(-446,-64),(-439,-67),(-424,-72),(-412,-77),(-399,-79),(-388,-81),(-381,-81),(-368,-78),(-355,-72),(-343,-65),(-333,-58),(-320,-50),(-303,-41),(-299,-38),(-288,-31),(-280,-26),(-273,-20),(-267,-15),(-260,-8),(-254,-4),(-248,-2),(-240,2),(-237,2),(-224,1),(-215,-2),(-204,-5),(-187,-10),(-164,-19),(-157,-23),(-149,-24),(-137,-26),(-123,-31),(-114,-33),(-99,-35),(-88,-37),(-72,-40),(-59,-42),(-53,-43),(-46,-43),(-40,-43),(-26,-43),(-17,-43),(-9,-40),(-1,-35),(12,-27),(19,-21),(25,-15),(38,-5),(48,1),(56,9),(65,16),(76,22),(102,34),(110,37),(125,42),(133,43),(150,45),(156,46),(169,47),(170,47),(183,44),(202,38),(215,35),(228,31),(242,26),(255,23),(276,16),(282,14),(300,10),(313,5),(331,-2),(350,-6),(356,-7),(377,-11),(385,-11),(394,-11),(403,-10),(416,-5),(431,-1),(444,6),(454,10),(465,16),(477,23),(486,31),(491,34),(500,40),(513,48),(518,53),(527,59),(536,65),(542,71),(551,78),(557,81),(566,87),(581,90),(585,92),(589,93),(593,96),(603,99),(614,102),(616,103),(620,105),(638,109)]
    points=brokenline(line)
    drawpoints(points, 9, 8, 59)
    fill(points, 9, 8, 59 -1)


    line=[(-638,-247),(-627,-243),(-611,-233),(-588,-218),(-579,-210),(-563,-200),(-548,-189),(-538,-181),(-528,-173),(-521,-167),(-511,-157),(-499,-143),(-496,-137),(-484,-125),(-481,-124),(-463,-123),(-455,-125),(-450,-128),(-446,-130),(-443,-133),(-437,-138),(-433,-140),(-429,-141),(-425,-141),(-411,-141),(-402,-139),(-389,-134),(-387,-129),(-375,-116),(-370,-110),(-366,-105),(-352,-94),(-345,-90),(-326,-81),(-317,-78),(-310,-76),(-298,-73),(-289,-70),(-278,-66),(-261,-59),(-252,-55),(-235,-49),(-221,-44),(-204,-36),(-191,-31),(-176,-27),(-160,-26),(-151,-26),(-134,-27),(-111,-29),(-102,-31),(-91,-34),(-65,-44),(-54,-49),(-38,-53),(-27,-56),(-11,-62),(4,-67),(21,-74),(37,-85),(52,-89),(61,-93),(73,-97),(85,-101),(100,-103),(109,-103),(122,-104),(139,-103),(155,-98),(173,-91),(190,-81),(204,-73),(220,-64),(229,-56),(241,-49),(247,-44),(272,-28),(275,-24),(280,-18),(288,-11),(295,-6),(303,0),(309,4),(316,8),(324,11),(338,11),(349,10),(358,10),(372,10),(384,10),(401,9),(424,5),(432,1),(439,-3),(447,-10),(451,-15),(457,-24),(463,-29),(468,-33),(478,-43),(481,-47),(486,-53),(491,-60),(496,-66),(501,-70),(507,-77),(509,-82),(516,-90),(527,-111),(534,-118),(538,-120),(545,-127),(553,-131),(556,-132),(557,-132),(565,-126),(573,-115),(585,-101),(594,-95),(597,-91),(610,-83),(618,-79),(626,-76),(632,-74),(634,-73),(638,-73)]
    points=brokenline(line)
    drawpoints(points, 3, 2, 46)
    fill(points, 3, 2, 46 -1)

    line=[(-638,-277),(-621,-277),(-614,-276),(-577,-277),(-567,-277),(-549,-280),(-531,-284),(-513,-286),(-475,-290),(-469,-290),(-424,-285),(-404,-279),(-389,-274),(-344,-269),(-327,-264),(-302,-260),(-280,-257),(-253,-257),(-219,-257),(-189,-257),(-156,-258),(-121,-261),(-94,-266),(-65,-269),(-38,-270),(-6,-270),(36,-268),(54,-266),(80,-260),(105,-254),(124,-252),(148,-248),(160,-244),(173,-240),(201,-238),(241,-242),(279,-246),(299,-247),(329,-252),(367,-262),(412,-270),(449,-272),(472,-272),(506,-272),(525,-270),(538,-268),(571,-262),(584,-261),(600,-260),(608,-260),(618,-260),(622,-260),(624,-260),(630,-261),(631,-261),(638,-261)]
    points=brokenline(line)
    drawpoints(points, 2, 1, 16)
    fill(points, 2, 1, 16 -1)




def background_starrynight():
    global frame

    #setting up the sky
    point=midpointlinedraw(-638, 358, 638, 358)
    drawpoints(point, 3, 2, 28)    
    fill(point, 3, 2, 28, -1) 

    #stars
    
    if frame%2==0:
        stars=[(-637,-277),(-621,-277),(-614,-276),(-577,-277),(-567,-277),(-549,-280),(-531,-284),(-513,-286),(-475,-290),(-469,-290),(-424,-285),(-404,-279),(-389,-274),(-344,-269),(-327,-264),(-302,-260),(-280,-257),(-253,-257),(-219,-257),(-189,-257),(-156,-258),(-121,-261),(-94,-266),(-65,-269),(-38,-270),(-6,-270),(36,-268),(54,-266),(80,-260),(105,-254),(124,-252),(148,-248),(160,-244),(173,-240),(201,-238),(241,-242),(279,-246),(299,-247),(329,-252),(367,-262),(412,-270),(449,-272),(472,-272),(506,-272),(525,-270),(538,-268),(571,-262),(584,-261),(600,-260),(608,-260),(618,-260),(622,-260),(624,-260),(630,-261),(631,-261),(632,-261),(-576,237),(-525,215),(-521,163),(-546,120),(-576,141),(-472,182),(-428,144),(-407,100),(-355,107),(-326,111),(-310,174),(-322,213),(-373,250),(-437,246),(-396,194),(-293,168),(-260,124),(-224,113),(-170,109),(-95,107),(-50,195),(-83,265),(-168,254),(-174,210),(-93,185),(-12,139),(63,138),(160,132),(220,142),(252,218),(212,280),(52,265),(7,245),(-1,215),(53,203),(114,211),(200,220),(237,194),(178,158),(88,169),(-18,211),(-78,265),(-182,272),(-268,252),(-306,207),(-252,178),(-148,177),(-17,192),(234,187),(359,217),(424,249),(504,273),(538,181),(524,152),(453,131),(412,154),(379,207),(341,278),(279,294),(161,305),(163,204),(184,162),(182,115),(155,90),(75,105),(11,157),(-36,200),(-84,247),(-158,271),(-212,271),(-292,253),(-325,215),(-365,138),(-411,87),(-502,70),(-588,102),(-594,133),(-573,190),(-536,265),(-546,292),(-602,293),(-606,290),(-388,-3),(-318,18),(-287,45),(-455,101),(-468,124),(-465,328),(-402,322),(-583,335),(-604,-16),(-598,36),(-503,28),(-344,0),(-85,66),(-130,165),(303,176),(369,122),(464,166),(469,214),(508,219),(443,268),(394,305),(479,302),(535,296),(581,307),(591,236),(592,141),(546,89),(482,73),(417,78),(367,135),(327,173),(282,154),(245,113),(220,79),(97,75),(115,134),(108,230),(151,238),(267,137),(-45,296),(-113,237),(-124,148),(-146,76),(-309,48),(-361,8),(-344,285),(-310,308),(-294,324),(-195,323),(-216,226),(-210,183),(-39,120),(101,309),(126,288),(-473,226),(-608,60),(-568,53),(-570,24),(-609,-39),(332,120),(302,246),(550,242),(601,173),(562,111),(495,114),(-487,279),(-475,239)]
        drawpoints(stars, 255, 255, 255)
    else:
        stars=[(-117,309),(-90,282),(-115,258),(-126,292),(-213,309),(-252,310),(-272,276),(-298,249),(264,100),(291,117),(316,145),(279,210),(268,181),(195,176),(143,192),(112,179),(60,153),(-17,114),(-64,93),(-136,81),(-400,-2),(-348,0),(-322,28),(-321,49),(-341,-33),(-356,19),(-594,252),(-597,217),(-601,161),(-539,159),(-527,111),(-464,69),(-445,45),(-445,6),(-442,43),(-385,46),(-555,54),(-509,58),(567,274),(528,272),(507,295),(535,308),(560,328),(619,298),(614,226),(607,186),(562,193),(596,221),(553,162),(502,101),(447,139),(499,185),(433,249),(411,199),(409,154),(271,131),(284,166),(345,203),(278,288),(213,225),(119,150),(214,189),(247,229),(275,168),(281,166),(270,133),(271,106),(266,84),(221,70),(152,71),(150,93),(161,159),(139,226),(77,277),(7,287),(-118,278),(-197,239),(-145,196),(-144,180),(-168,141),(-198,114),(-246,94),(-360,84),(-392,84),(-480,54),(-425,31),(-403,21),(-384,7),(-361,7),(-348,44),(-347,64),(-409,108),(-472,207),(-448,281),(-423,286),(-418,228),(-463,194),(-407,140),(-299,159),(-201,266),(-198,177),(-199,90),(-51,145),(178,233),(-71,255),(99,271),(137,204),(130,148),(322,163),(-69,187),(-73,149),(223,101),(292,149),(-535,266),(-539,233),(-510,215),(-497,187),(-482,129),(-445,127),(-437,144),(-454,136),(-455,132),(-346,199),(-330,285),(-376,293),(-365,224),(-308,219),(-326,282),(-361,233),(-327,192),(-322,206),(-209,290),(-305,270),(-306,230),(394,300),(361,275),(333,242),(293,237),(271,250),(251,273),(211,295),(175,297),(152,294),(103,268),(-16,232),(2,242),(34,220),(32,188),(11,184),(-23,202),(-30,220),(28,248),(68,229),(70,193),(18,172),(-43,160),(6,166),(50,231),(54,212),(67,169),(60,172),(81,101),(97,87),(97,70),(79,92),(87,108),(116,87),(333,312),(422,317),(426,280),(353,258),(312,261),(318,204),(357,221),(391,187),(412,131),(393,115),(371,118),(378,147),(448,177),(437,210),(415,282),(369,273),(339,181),(303,130),(305,154),(377,84),(381,85),(441,169),(-605,16),(-602,74),(-599,75),(-612,25),(-614,6),(-569,46),(-583,116),(-583,148),(-578,313),(-541,321),(-533,322),(-559,159),(-507,182),(-431,245),(-446,252),(-463,188),(-454,130),(-454,82),(-464,72),(-484,120),(-426,160),(-327,201),(-318,228),(-386,233),(-439,195),(-394,127),(-261,202),(-217,217),(-184,259),(-189,285),(-197,281),(-209,212),(-195,166),(-176,163),(-41,280),(-79,268),(-96,246),(-91,225),(-53,220),(-28,211),(-20,183),(-39,154),(-64,148),(-99,163),(-100,169),(77,135),(87,167),(89,182),(91,233),(91,266),(91,266),(87,223),(91,161),(92,113),(91,152),(97,180),(112,190),(136,171),(147,140),(152,131),(160,127),(183,138),(235,182),(195,181),(181,142),(238,116),(255,126),(302,227),(299,263),(268,216),(280,152),(290,129),(342,160),(382,266),(382,273),(371,181),(382,104),(376,195),(409,212),(438,192),(394,147),(379,147),(-382,181),(-350,142),(-335,127),(-304,104),(-276,108),(-254,125),(-237,142),(-228,154),(-267,163),(-263,256),(-237,266),(-239,248),(-240,243),(-303,36),(-265,72),(-284,101),(-301,112),(-329,118),(-349,131),(-361,145),(-370,162),(-360,182),(-348,173),(-318,146),(-293,128),(-265,114),(-244,134),(-237,153),(-219,169),(589,274),(584,189),(582,129),(541,133),(545,175),(559,189),(464,282),(490,265),(502,263),(526,245),(533,221),(526,178),(517,126),(490,156),(500,180),(510,255),(476,272),(460,222),(476,148),(475,103),(446,91),(455,104),(-471,330),(-452,307),(-439,297),(-373,303),(-365,328),(-306,317),(-277,297),(-237,283),(-205,305),(-272,323),(-223,296),(-75,308),(69,306),(-59,266),(-59,323),(88,322),(289,297),(384,297),(465,313),(472,311),(567,243),(539,259),(566,311),(466,294),(499,218),(-85,47),(-137,73),(-143,96),(-115,113),(-81,115),(-59,128),(-46,112),(-42,77),(-58,64),(-102,57),(-144,54),(-161,54),(-172,56),(-172,71),(-201,76),(-228,91),(-258,90),(-424,56),(-437,45),(-413,39),(-617,-55),(-605,-53),(-589,-17),(-611,-26),(436,78),(464,76),(484,84),(436,104),(444,118),(462,121),(542,286),(532,212),(559,170),(470,214),(476,266),(527,290),(502,299),(514,239),(528,225),(481,198),(523,218),(537,158),(554,169),(561,138)]
        drawpoints(stars, 255, 255, 255)
    

    line=[(-638,-115),(-480,-3),(-440,-24),(-420,-36),(-384,-51),(-372,-56),(-346,-53),(-340,-52),(-317,-40),(-301,-26),(-292,-16),(-266,14),(-258,27),(-253,38),(-251,40),(-226,57),(-220,63),(-208,50),(-195,37),(-183,15),(-175,6),(-162,-10),(-151,-26),(-145,-31),(-135,-42),(-123,-59),(-121,-63),(-119,-64),(-105,-61),(-99,-51),(-88,-35),(-74,-12),(-70,-6),(-64,5),(-46,31),(-40,44),(-20,63),(-5,80),(-1,85),(19,96),(27,91),(40,75),(51,66),(60,54),(65,40),(71,28),(78,17),(91,2),(101,-8),(114,-9),(122,-9),(131,-9),(140,-7),(146,-4),(158,3),(171,9),(186,10),(203,10),(206,10),(223,0),(233,-9),(248,-22),(264,-35),(268,-36),(277,-41),(292,-47),(294,-48),(308,-49),(323,-47),(339,-38),(350,-31),(356,-25),(375,-10),(385,-2),(391,2),(409,14),(415,17),(435,35),(441,39),(448,43),(463,52),(474,55),(484,56),(490,56),(499,50),(508,38),(512,30),(514,25),(518,18),(521,13),(530,10),(536,10),(542,15),(550,24),(555,31),(558,36),(560,36),(566,24),(570,16),(578,1),(587,-8),(591,-14),(598,-24),(602,-33),(605,-43),(616,-66),(618,-71),(619,-77),(621,-88),(630,-103),(631,-106),(638,-107)]
    points=brokenline(line)
    drawpoints(points, 9, 8, 59)
    fill(points, 9, 8, 59, -1)
    
    line=[(-638,-138),(-623,-125),(-612,-104),(-600,-79),(-599,-72),(-586,-44),(-574,-30),(-563,-11),(-558,-3),(-545,5),(-541,6),(-534,5),(-518,-7),(-511,-14),(-507,-17),(-499,-24),(-493,-28),(-489,-30),(-486,-34),(-482,-37),(-478,-38),(-470,-39),(-465,-39),(-462,-39),(-458,-39),(-452,-40),(-445,-41),(-440,-44),(-434,-49),(-415,-55),(-407,-59),(-381,-70),(-374,-72),(-351,-76),(-331,-75),(-319,-71),(-296,-55),(-284,-47),(-272,-39),(-265,-32),(-259,-27),(-243,-17),(-232,-11),(-219,0),(-201,15),(-193,20),(-182,28),(-174,35),(-167,40),(-163,41),(-153,44),(-131,44),(-127,44),(-91,30),(-81,26),(-73,22),(-47,5),(-40,2),(-6,-13),(5,-18),(28,-28),(41,-35),(78,-40),(88,-40),(114,-38),(133,-31),(152,-22),(171,-10),(185,-2),(202,11),(218,23),(227,29),(247,41),(259,50),(271,57),(284,64),(302,78),(314,92),(329,100),(336,104),(336,104),(337,100),(341,91),(344,73),(347,67),(349,61),(350,53),(356,45),(360,44),(373,52),(380,56),(387,59),(403,64),(404,64),(416,54),(428,43),(441,22),(446,18),(456,7),(466,-1),(468,-2),(473,-5),(480,-11),(492,-22),(500,-26),(507,-27),(518,-22),(530,-12),(534,-8),(538,-7),(544,-12),(547,-24),(550,-31),(554,-35),(561,-30),(569,-21),(583,-14),(591,-7),(597,-1),(600,-2),(606,-11),(608,-15),(612,-22),(616,-28),(619,-35),(621,-39),(623,-41),(624,-41),(638,-41)]
    points=brokenline(line)
    drawpoints(points, 3, 2, 46)
    fill(points, 3, 2, 46 -1)
    
    line=[(-638,-178),(-613,-167),(-603,-158),(-589,-140),(-573,-122),(-559,-106),(-538,-92),(-524,-79),(-511,-68),(-500,-63),(-483,-61),(-472,-61),(-455,-62),(-446,-64),(-439,-67),(-424,-72),(-412,-77),(-399,-79),(-388,-81),(-381,-81),(-368,-78),(-355,-72),(-343,-65),(-333,-58),(-320,-50),(-303,-41),(-299,-38),(-288,-31),(-280,-26),(-273,-20),(-267,-15),(-260,-8),(-254,-4),(-248,-2),(-240,2),(-237,2),(-224,1),(-215,-2),(-204,-5),(-187,-10),(-164,-19),(-157,-23),(-149,-24),(-137,-26),(-123,-31),(-114,-33),(-99,-35),(-88,-37),(-72,-40),(-59,-42),(-53,-43),(-46,-43),(-40,-43),(-26,-43),(-17,-43),(-9,-40),(-1,-35),(12,-27),(19,-21),(25,-15),(38,-5),(48,1),(56,9),(65,16),(76,22),(102,34),(110,37),(125,42),(133,43),(150,45),(156,46),(169,47),(170,47),(183,44),(202,38),(215,35),(228,31),(242,26),(255,23),(276,16),(282,14),(300,10),(313,5),(331,-2),(350,-6),(356,-7),(377,-11),(385,-11),(394,-11),(403,-10),(416,-5),(431,-1),(444,6),(454,10),(465,16),(477,23),(486,31),(491,34),(500,40),(513,48),(518,53),(527,59),(536,65),(542,71),(551,78),(557,81),(566,87),(581,90),(585,92),(589,93),(593,96),(603,99),(614,102),(616,103),(620,105),(638,109)]
    points=brokenline(line)
    drawpoints(points, 9, 8, 59)
    fill(points, 9, 8, 59 -1)

    line=[(-638,-247),(-627,-243),(-611,-233),(-588,-218),(-579,-210),(-563,-200),(-548,-189),(-538,-181),(-528,-173),(-521,-167),(-511,-157),(-499,-143),(-496,-137),(-484,-125),(-481,-124),(-463,-123),(-455,-125),(-450,-128),(-446,-130),(-443,-133),(-437,-138),(-433,-140),(-429,-141),(-425,-141),(-411,-141),(-402,-139),(-389,-134),(-387,-129),(-375,-116),(-370,-110),(-366,-105),(-352,-94),(-345,-90),(-326,-81),(-317,-78),(-310,-76),(-298,-73),(-289,-70),(-278,-66),(-261,-59),(-252,-55),(-235,-49),(-221,-44),(-204,-36),(-191,-31),(-176,-27),(-160,-26),(-151,-26),(-134,-27),(-111,-29),(-102,-31),(-91,-34),(-65,-44),(-54,-49),(-38,-53),(-27,-56),(-11,-62),(4,-67),(21,-74),(37,-85),(52,-89),(61,-93),(73,-97),(85,-101),(100,-103),(109,-103),(122,-104),(139,-103),(155,-98),(173,-91),(190,-81),(204,-73),(220,-64),(229,-56),(241,-49),(247,-44),(272,-28),(275,-24),(280,-18),(288,-11),(295,-6),(303,0),(309,4),(316,8),(324,11),(338,11),(349,10),(358,10),(372,10),(384,10),(401,9),(424,5),(432,1),(439,-3),(447,-10),(451,-15),(457,-24),(463,-29),(468,-33),(478,-43),(481,-47),(486,-53),(491,-60),(496,-66),(501,-70),(507,-77),(509,-82),(516,-90),(527,-111),(534,-118),(538,-120),(545,-127),(553,-131),(556,-132),(557,-132),(565,-126),(573,-115),(585,-101),(594,-95),(597,-91),(610,-83),(618,-79),(626,-76),(632,-74),(634,-73),(638,-73)]
    points=brokenline(line)
    drawpoints(points, 3, 2, 46)
    fill(points, 3, 2, 46 -1)

    line=[(-638,-277),(-621,-277),(-614,-276),(-577,-277),(-567,-277),(-549,-280),(-531,-284),(-513,-286),(-475,-290),(-469,-290),(-424,-285),(-404,-279),(-389,-274),(-344,-269),(-327,-264),(-302,-260),(-280,-257),(-253,-257),(-219,-257),(-189,-257),(-156,-258),(-121,-261),(-94,-266),(-65,-269),(-38,-270),(-6,-270),(36,-268),(54,-266),(80,-260),(105,-254),(124,-252),(148,-248),(160,-244),(173,-240),(201,-238),(241,-242),(279,-246),(299,-247),(329,-252),(367,-262),(412,-270),(449,-272),(472,-272),(506,-272),(525,-270),(538,-268),(571,-262),(584,-261),(600,-260),(608,-260),(618,-260),(622,-260),(624,-260),(630,-261),(631,-261),(638,-261)]
    points=brokenline(line)
    drawpoints(points, 2, 1, 16)
    fill(points, 2, 1, 16 -1)

    pass
