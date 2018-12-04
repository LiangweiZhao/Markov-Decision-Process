import numpy as np
import time
S = 0  #Stay position
T = 1  #Direction to top
L = 2  #Direction to left
B = 3  #Direction to bottom
R = 4  #Direction to right
df = 0.9 #Discont Featrue
tm = 0.1*(0.1)/0.9 #use to terminate
#Get the cost 2d array of each car
def getCost2dArr(car):
    init2dArr[end[car].getX()][end[car].getY()] += 100
    return init2dArr.copy()
#The transition possibility
def P(x0,y0,x1,y1,action):
    if action == L:
        if y1 == y0-1:
            return 0.7
        else:
            return 0.1
    elif action == R:
        if y1 == y0+1:
            return 0.7
        else:
            return 0.1
    elif action == T:
        if x1 == x0-1:
            return 0.7
        else:
            return 0.1
    elif action == B:
        if x1 == x0+1:
            return 0.7
        else:
            return 0.1
#Calculate the Ui-1
def getLastU(action,x,y,lastU2dArr):
    #North
    if y-1 < 0:
        cost1 = lastU2dArr[x][y]
    else:
        cost1 = lastU2dArr[x][y-1]
    #South
    if y+1 >= size:
        cost2 = lastU2dArr[x][y]
    else:
        cost2 = lastU2dArr[x][y+1]
    #East
    if x+1 >= size:
        cost3 = lastU2dArr[x][y]
    else:
        cost3 = lastU2dArr[x+1][y]
    #West
    if x-1 < 0:
        cost4 = lastU2dArr[x][y]
    else:
        cost4 = lastU2dArr[x-1][y]

    return cost1 * P(x,y,x,y-1,action) + cost2 * P(x,y,x,y+1,action) + cost3 * P(x,y,x+1,y,action) + cost4 * P(x,y,x-1,y,
                                                                                                               action)
#Get the policy direction of each car
def getPolicy(car):
    endPoint = end[car]
    cost2dArr = costDict[car]
    curU_dict = {}
    curU_dict[0] = np.zeros(shape=(size,size),dtype=np.float64)
    #curU_dict[0] = np.array(tmp2dArr,dtype=np.float64)
    dirt2dArr = np.ones(shape=(size,size),dtype=np.float64)
    times = 0
    # Calculate the direction of each nodes with MDP
    while True:
        #curU
        tmpU2dArr = curU_dict[times].copy()
        maxChange = 0
        for j in range(size):
            for i in range(size):
                if i == endPoint.getX() and j == endPoint.getY():
                    tmpU2dArr[i][j] = cost2dArr[i][j]
                    continue
                maxDict = T
                maxU = getLastU(T,i,j,curU_dict[times])
                for k in range(2,5):
                    k = order[k]
                    tmpVal = getLastU(k,i,j, curU_dict[times])
                    if tmpVal > maxU:
                        maxU = tmpVal
                        maxDict = k
                dirt2dArr[i][j] = maxDict
                tmpU2dArr[i][j] = cost2dArr[i][j] + df * maxU
                maxChange = max(abs(tmpU2dArr[i][j]-curU_dict[times][i][j]),maxChange)
        # Terminate
        if maxChange < tm:
            return dirt2dArr
        # times
        times += 1
        curU_dict[times] = tmpU2dArr

#Change the direction
def turn_left(move):
    move += 1 #change the direction by 90 degree(counter-clockwise)
    if move == 5:
        move = T
    return move
def turn_right(move):
    move -= 1
    if(move == 0):
        move = R
    return move
def to_back(move):
    if move == 1:
        move = 3
    elif move == 2:
        move = 4
    elif move == 3:
        move = 1
    elif move == 4:
        move = 2
    return move


class Point:
    def __init__(self,x,y,parent=None):
        self.X = x
        self.Y = y
        self.parent = parent
    def __str__(self):
        return "(%s,%s)"%(self.X,self.Y)
    def __repr__(self):
        return str(self)
    def __ne__(self, other):
        if other != None:
            return self.getX() != other.getX() or self.getY() != other.getY()
        else:
            return True
    def __eq__(self, other):
        if other != None:
            return self.getX() == other.getX() and self.getY() == other.getY()
        else:
            return False
    #Get the X coordinate of Point
    def getX(self):
        return self.X
    #Get the Y coordinate of Point
    def getY(self):
        return self.Y
    #Turn to north
    def toNorth(self):
        return Point(self.X,self.Y - 1)
    #Turn to south
    def toSouth(self):
        return Point(self.X, self.Y + 1)
    #Turn to west
    def toWest(self):
        return Point(self.X - 1 , self.Y)
    #Turn to east
    def toEast(self):
        return Point(self.X + 1, self.Y)
    def to(self,other):
        return abs(self.getX()-other.getX())+abs(self.getY()-other.getY())
    def addParent(self,other):
        self.parent = other
    def illegal(self):
        return self.X < 0 or self.Y < 0 or self.X >= size or self.Y >= size


start = time.clock()
input_file = open('input2.txt','r')
output_file = open('output.txt','w')
#Read input
size = int(input_file.readline())
carNum = int(input_file.readline())
obstacles = int(input_file.readline())
obsArr = []
for i in range(obstacles):
    tmpInput = input_file.readline().strip().split(',')
    obsArr.append(Point(int(tmpInput[1]),int(tmpInput[0])))
cars = []
end = []
for i in range(carNum):
    tmpInput = input_file.readline().strip().split(',')
    cars.append(Point(int(tmpInput[1]),int(tmpInput[0])))
for i in range(carNum):
    tmpInput = input_file.readline().strip().split(',')
    end.append(Point(int(tmpInput[1]),int(tmpInput[0])))

#Cost for all nodes
#init2dArr = [[-1 for x in range(size)] for y in range(size)]
init2dArr = -1*np.ones(shape=(size,size),dtype=np.float64)
for i in range(obstacles):  #set obstacles
    init2dArr[obsArr[i].getX()][obsArr[i].getY()] -= 100
costDict = {}
for i in range(carNum):
    costDict[i] = getCost2dArr(i)
    init2dArr[end[i].getX()][end[i].getY()] = -1
#print costDict[0]
#order of direction: T:1,S:3,E:4,W:2
order=[0,1,3,4,2]
#Get policies
policies = {}
for i in range(carNum):
    policies[i] = getPolicy(i)
#Calculate Points
ave = []
stay = False
stayCost = 0
print time.clock() - start
for i in range(len(cars)):
    sum = 0
    costArr = costDict[i]
    for j in range(10):
        pos = cars[i]
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k = 0
        while pos != end[i]:
            move = policies[i][pos.getX()][pos.getY()]
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = to_back(move)
                    else:
                        #move = turn_left(move)
                        #move = to_back(move, pos)
                        move = turn_right(move)
                else:
                    #move = turn_right(move)
                    #move = to_back(move, pos)
                    move = turn_left(move)
            k += 1
            if move == L:
                if not pos.toNorth().illegal():
                    pos = pos.toNorth()
                sum += costArr[pos.getX()][pos.getY()]
            elif move == T:
                if not pos.toWest().illegal():
                    pos = pos.toWest()
                sum += costArr[pos.getX()][pos.getY()]
            elif move == R:
                if not pos.toSouth().illegal():
                    pos = pos.toSouth()
                sum += costArr[pos.getX()][pos.getY()]
            elif move == B:
                if not pos.toEast().illegal():
                    pos = pos.toEast()
                sum += costArr[pos.getX()][pos.getY()]
    ave.append(int(np.floor(sum/10.0)))
for i in ave:
    output_file.write(str(i)+'\n')
#print policies
for i in range(len(policies)):
    print (policies[i])
print ave
print time.clock()-start