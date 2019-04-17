import traceback, turtle, time, math

#float value representing amount of time, in seconds, to delay after
#   each time the tree changes.  Adjust as you wish, but set it back
#   to 0.0 before submitting.
draw_delay = 0.0

#Set this to False to turn off turtle entirely.
enable_turtle = True

#insert_floor: Takes FloorTree (BST) object floor_tree, and FloorNode object
#   floor, and inserts floor into floor_tree.  Doesn't return anything.
def insert_floor(floor_tree,floor):
    cur = floor_tree.root
    prev = None
    while cur != None:
        prev = cur
        if floor.floor_num < cur.floor_num: cur = cur.left
        else: cur = cur.right
    floor.parent = prev
    if prev == None:
        floor_tree.root = floor
    elif floor.floor_num < prev.floor_num:
        prev.left = floor
    else: prev.right = floor
    return

#delete_floor: Takes FloorTree (BST) object floor_tree, and FloorNode object
#   floor, and removes floor from floor_tree, if present.  Returns nothing.
def delete_floor(floor_tree,floor):
    if floor.left == None: transplant(floor_tree,floor,floor.right)
    elif floor.right == None: transplant(floor_tree,floor,floor.left)
    else:
        suc = tree_minimum(floor.right)
        if suc.parent != floor:
            transplant(floor_tree,suc,suc.right)
            suc.right = floor.right
            suc.right.parent = suc
        transplant(floor_tree,floor,suc)
        suc.left = floor.left
        suc.left.parent = floor.left
    return

#find_nearest_unhaunted: Takes FloorTree (BST) object floor_tree, and an
#   integer floor_num.  Returns the FloorNode object within the tree with
#   floor number closest to the specified value.
#This is basically BST_Serach but with the added twist that you have to
#   return the closest node in the case that the search query is not
#   found within the tree.
def find_nearest_unhaunted(floor_tree,floor_num):
    cur = floor_tree.root
    prev = None
    double_prev = None
    while cur != None:
        if cur.floor_num < floor_num:
            double_prev = prev
            prev = cur
            cur = cur.right
        elif cur.floor_num > floor_num:
            double_prev = prev
            prev = cur
            cur = cur.left
        else: return cur
    if cur == None:
        if abs(floor_num - double_prev.floor_num) < abs(floor_num - prev.floor_num):
            return double_prev
        else: return prev
    return cur

def transplant(floor_tree,old,new):
    if old.parent == None: floor_tree.root = new
    elif old == old.parent.left: old.parent.left = new
    else: old.parent.right = new
    if new != None: new.parent = old.parent
    return

def tree_minimum(floor_tree):
    cur = floor_tree
    prev = None
    while cur != None:
        prev = cur
        cur = cur.left
    return prev


#DO NOT EDIT BELOW THIS LINE

#FloorNode class: represents a single node within the BST.  Contains
#   several instance variables.
#.floor_num: The floor number for this node, i.e. the key within the BST.
#.left: pointer to another FloorNode object representing the left
#   child of this node within the BST.
#.right: pointer to another FloorNode object representing the right
#   child of this node within the BST.
#.parent: pointer to another FloorNode object representing the parent
#   of this node within the BST.
#
#The following instance variables are for Turtle graphics only
#.x: float representing the x-coordinate of this node when drawn
#.y: float representing the y-coordinate of this node when drawn
#.position: the array index of this node if this was a heap implementation
#   Used for determination of .x and .y
#.t: Turtle object used to draw this node.
class FloorNode:
    def __init__(self,floor_num,t):
        self.floor_num = floor_num
        self.left = None
        self.right = None
        self.parent = None
        self.x = 0
        self.y = 0
        self.position = 1
        self.t = t
    def draw_node_num(self):
        self.t.penup()
        self.t.setpos(self.x,self.y-10)
        self.t.pendown()
        self.t.color("white")
        self.t.write(self.floor_num,align="center",font=("Arial",15,"normal"))
    def draw_node(self):
        level = int(math.log2(float(self.position)))
        left_level = 160 - 160 + 10*(2**(4-level))
        over = self.position - 2**level
        self.x = left_level + over*20*(2**(4-level))
        self.y = 100 - level*50 + 10
        self.t.penup()
        self.t.setpos(self.x,self.y-10)
        self.t.pendown()
        self.t.color("black")
        self.t.begin_fill()
        self.t.circle(10)
        self.t.end_fill()
        self.t.color("white")
    def draw_edge(self,other):
        if self == other or other == None:
            return
        dx = other.x - self.x
        dy = other.y - self.y
        dist = (dx*dx+dy*dy)**(0.5)
        sx = dx*(10/dist)
        sy = dy*(10/dist)
        startx = self.x+sx
        starty = self.y+sy
        endx = other.x-sx
        endy = other.y-sy
        self.t.penup()
        self.t.setpos(startx,starty)
        self.t.pendown()
        self.t.color("black")
        self.t.setpos(endx,endy)
    def draw_recurse(self):
        self.draw_node()
        if self.left != None:
            self.left.position = self.position*2
            self.left.draw_recurse()
            self.draw_edge(self.left)
        if self.right != None:
            self.right.position = self.position*2+1
            self.right.draw_recurse()
            self.draw_edge(self.right)
        self.draw_node_num()
    def __repr__(self):
        return "F"+str(self.floor_num)
    def __eq__(self,other):
        return type(other) == FloorNode and self.floor_num == other.floor_num
    def eq_recurse(self,other,failstring):
        if self != other:
            print("Node",failstring,"incorrect - Expected:",
                  self,"\nGot     :",other)
            return False
        if self.left == None:
            if other.left != None:
                print("Node",failstring+".left","incorrect - Expected:",
                  None,"\nGot     :",other.left)
                return False
            return True
        leftEq = self.left.eq_recurse(other.left,failstring+".left")
        if self.right == None:
            if other.right != None:
                print("Node",failstring+".right","incorrect - Expected:",
                  None,"\nGot     :",other.right)
                return False
            return True
        rightEq = self.right.eq_recurse(other.right,failstring+".right")
        return leftEq and rightEq

#FloorTree class: represents the BST as a whole.  Mostly exists
#   just to provide a pointer to the root of the BST, and to do BST
#   equality checks.
class FloorTree:
    def __init__(self,root):
        self.root = root
    def draw_tree(self):
        if self.root != None:
            self.root.position = 1
            self.root.draw_recurse()
    def __eq__(self,other):
        if type(other) != FloorTree:
            return False
        if self.root == None:
            if other.root != None:
                print("Node","root","incorrect - Expected:",
                  None,"\nGot     :",other.root)
            return (other.root == None)
        return self.root.eq_recurse(other.root,"root")


#Turtle/Test case setup functions
if enable_turtle:
    draw_turtle = turtle.Turtle()
    draw_turtle.speed(0)
    draw_turtle.hideturtle()
else:
    draw_turtle = None

def construct_test(ls,draw_turtle):
    for i in range(1,len(ls)):
        if ls[i] != None:
            ls[i] = FloorNode(ls[i],draw_turtle)
            parent = ls[i//2]
            ls[i].parent = parent
            if i != 1 and i % 2 == 1:
                parent.right = ls[i]
            elif i % 2 == 0:
                parent.left = ls[i]
    return FloorTree(ls[1])

def draw_floor_nums(ls,draw_turtle,requested,elevator):
    for i in range(20):
        xpos = -200
        ypos = -200+i*20
        draw_turtle.penup()
        draw_turtle.setpos(xpos-20,ypos)
        draw_turtle.pendown()
        draw_turtle.color("black")
        if (i+1) == requested:
            draw_turtle.color("yellow")
        draw_turtle.write(str(i+1),align="center",
                          font=("Arial",15,"normal"))

def draw_elevator(ls,draw_turtle,requested,elevator):
    for i in range(20):
        xpos = -200
        ypos = -200+i*20
        draw_turtle.penup()
        draw_turtle.setpos(xpos,ypos)
        draw_turtle.pendown()
        draw_turtle.color("grey")
        if (i+1) == requested:
            draw_turtle.color("yellow")
        draw_turtle.fillcolor("black")
        draw_turtle.begin_fill()
        for j in range(2):
            draw_turtle.forward(100)
            draw_turtle.left(90)
            draw_turtle.forward(20)
            draw_turtle.left(90)
        draw_turtle.end_fill()
        draw_turtle.setpos(xpos+20,ypos)
        if ls[i]:
            draw_turtle.penup()
            draw_turtle.setpos(xpos+50,ypos+2)
            draw_turtle.color("white")
            draw_turtle.begin_fill()
            draw_turtle.pendown()
            for i in range(4):
                draw_turtle.forward(10)
                draw_turtle.left(90)
            draw_turtle.end_fill()
            draw_turtle.setpos(xpos+55,ypos+7)
            draw_turtle.begin_fill()
            draw_turtle.circle(5)
            draw_turtle.end_fill()
            draw_turtle.setpos(xpos+56,ypos+12)
            draw_turtle.color("black")
            draw_turtle.setpos(xpos+56,ypos+15)
            draw_turtle.penup()
            draw_turtle.setpos(xpos+58,ypos+12)
            draw_turtle.pendown()
            draw_turtle.setpos(xpos+58,ypos+15)
        if (i+1) == elevator:
            draw_turtle.penup()
            draw_turtle.setpos(xpos+105,ypos+2)
            draw_turtle.pendown()
            draw_turtle.color("black")
            draw_turtle.fillcolor("grey")
            draw_turtle.begin_fill()
            for i in range(4):
                draw_turtle.forward(18)
                draw_turtle.left(90)
            draw_turtle.end_fill()
            draw_turtle.forward(9)
            draw_turtle.left(90)
            draw_turtle.forward(18)
            draw_turtle.color("brown")
            draw_turtle.pensize(2)
            draw_turtle.setpos(xpos+114,200)
            draw_turtle.left(270)
            draw_turtle.color("black")
            draw_turtle.pensize(1)


def wipe_screen(draw_turtle):
    draw_turtle.color("white")
    draw_turtle.setpos(-150,-250)
    draw_turtle.begin_fill()
    for i in range(4):
        draw_turtle.forward(500)
        draw_turtle.left(90)
    draw_turtle.end_fill()

#Test cases

floor_list1 = [8,10,1]
corrls_1 = [None,8,1,10]
correct_1 = construct_test(corrls_1,draw_turtle)
del_1 = corrls_1[2]
corrls_1d = [None,8,None,10]
correct_1d = construct_test(corrls_1d,draw_turtle)
ser_1 = 10
correct_1s = corrls_1d[3]

floor_list2 = [17,15,11,1]
corrls_2 = [None,17,15,None,11,None,None,None,1]
correct_2 = construct_test(corrls_2,draw_turtle)
del_2 = corrls_2[2]
corrls_2d = [None,17,11,None,1]
correct_2d = construct_test(corrls_2d,draw_turtle)
ser_2 = 15
correct_2s = corrls_2d[1]

floor_list3 = [11,3,7,18,1]
corrls_3 = [None,11,3,18,1,7]
correct_3 = construct_test(corrls_3,draw_turtle)
del_3 = corrls_3[1]
corrls_3d = [None,18,3,None,1,7]
correct_3d = construct_test(corrls_3d,draw_turtle)
ser_3 = 4
correct_3s = corrls_3d[2]

floor_list4 = [1,11,19,12,16,10]
corrls_4 = [None,1,None,11,None,None,10,19,None,None,None,None,
            None,None,12,None,None,None,None,None,None,None,None,None,
            None,None,None,None,None,16,None,None]
correct_4 = construct_test(corrls_4,draw_turtle)
del_4 = corrls_4[3]
corrls_4d = [None,1,None,12,None,None,10,19,None,None,None,None,
            None,None,16]
correct_4d = construct_test(corrls_4d,draw_turtle)
ser_4 = 12
correct_4s = corrls_4d[3]

floor_list5 = [20, 12, 6, 11, 1, 13, 16]
corrls_5 = [None,20,12,None,6,13,None,None,1,11,None,16]
correct_5 = construct_test(corrls_5,draw_turtle)
del_5 = corrls_5[1]
corrls_5d = [None,12,6,13,1,11,None,16]
correct_5d = construct_test(corrls_5d,draw_turtle)
ser_5 = 19
correct_5s = corrls_5d[7]

floor_list6 = [6,19,7,1,14,17,3,8]
corrls_6 = [None,6,1,19,None,3,7,None,None,None,None,None,
            None,14,None,None,None,None,None,None,None,None,None,None,
            None,None,8,17]
correct_6 = construct_test(corrls_6,draw_turtle)
del_6 = corrls_6[1]
corrls_6d = [None,7,1,19,None,3,14,None,None,None,None,None,8,17]
correct_6d = construct_test(corrls_6d,draw_turtle)
ser_6 = 7
correct_6s = corrls_6d[1]


testlists = [floor_list1,floor_list2,floor_list3,floor_list4,
             floor_list5,floor_list6]
for i in range(len(testlists)):
    testlists[i] = list(map(lambda x: FloorNode(x,draw_turtle),testlists[i]))
correct = [correct_1,correct_2,correct_3,correct_4,correct_5,correct_6]
correct_d = [correct_1d,correct_2d,correct_3d,correct_4d,correct_5d,correct_6d]
del_list = [del_1,del_2,del_3,del_4,del_5,del_6]
correct_s = [correct_1s,correct_2s,correct_3s,correct_4s,correct_5s,correct_6s]
search_list = [ser_1,ser_2,ser_3,ser_4,ser_5,ser_6]

count = 0

try:
    for i in range(len(testlists)):
        print("\n---------------------------------------\n")
        print("TEST #",i+1,":")
        testlist = list(testlists[i])
        floor_tree = FloorTree(None)
        ghosts = [True]*20
        if enable_turtle:
            turtle.clearscreen()
            turtle.tracer(0,0)
            draw_floor_nums(ghosts,draw_turtle,0,0)
        #Insert a series of nodes
        for floor in testlist:
            print("Ghosts clear on",floor,": inserting node")
            insert_floor(floor_tree,floor)
            ghosts[floor.floor_num-1] = False
            if enable_turtle:
                wipe_screen(draw_turtle)
                draw_elevator(ghosts,draw_turtle,0,0)
                floor_tree.draw_tree()
                turtle.update()
                time.sleep(draw_delay)
        #Check that resulting tree is correct
        assert correct[i] == floor_tree, "Tree incorrect"
        floor_tree = correct[i]
        #Delete a node
        print("Ghosts detected on",del_list[i],": deleting node")
        delete_floor(floor_tree,del_list[i])
        ghosts[del_list[i].floor_num-1] = True
        if enable_turtle:
            wipe_screen(draw_turtle)
            draw_elevator(ghosts,draw_turtle,0,0)
            floor_tree.draw_tree()
            turtle.update()
            time.sleep(draw_delay)
        #Check that resulting tree is correct
        assert correct_d[i] == floor_tree, "Tree incorrect"
        floor_tree = correct_d[i]
        target = search_list[i]
        #Search for nearest floor devoid of ghosts to requested floor
        print("Elevator request: F"+str(target))
        actual = find_nearest_unhaunted(floor_tree,target)
        print("Elevator routed to:",actual)
        if enable_turtle:
            wipe_screen(draw_turtle)
            draw_elevator(ghosts,draw_turtle,target,actual.floor_num)
            floor_tree.draw_tree()
            draw_floor_nums(ghosts,draw_turtle,target,1)
            turtle.update()
            time.sleep(draw_delay)
        #Check return value of nearest unhaunted
        assert correct_s[i] == actual,\
               "Nearest unhaunted floor not returned - \nExpected: " + \
               str(correct_s[i]) + "\nGot:      " + str(actual)
        count += 1
except AssertionError as e:
    print("\nFAIL: ",e)
except Exception:
    print("\nFAIL: ",traceback.format_exc())


print("\n---------------------------------------\n")
print(count,"out of",6,"tests passed.")
