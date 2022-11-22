import random
import turtle
import time
wheels = ['FL','FR','BR']
sleepy = .01
Gx = random.randint(-600,600)
Gy = random.randint(-540,540)
goal = Gx,Gy
obs = 30
Ox=[]
Oy=[]
for i in range(obs):
    Ox.append(random.randint(-600,600))
    Oy.append(random.randint(-540,540))


class robot:
    def __init__(self, wheels):
        self.wheels = wheels
        self.sensorReadings = []
        self.timer=0
        self.timerlength=0
        self.s = turtle.getscreen()
        self.t = turtle.Turtle()
        self.t.shape("turtle")
        self.t.color("green")
        self.g = turtle.Turtle()
        self.g.penup()
        self.g.shape("circle")
        self.g.color("gold")
        self.g.goto(Gx, Gy)
        self.objects=[]
        self.sRange =300
        self.hRange = 50
        self.tempThreshold = 80
        self.soundVolume = 0
        for i in range (obs):
            self.objects.append(turtle.Turtle())
            self.objects[i].penup()
            self.objects[i].shape("square")
            self.objects[i].color("red")
            self.objects[i].goto(Ox[i],Oy[i])
    
    def checkWheels(self):
        while len(wheels) != 4:
            twheel = []
            print("The robot should have 4 wheels")
            for i in range (4):
                string="what is wheel " + str(i) + " called?\n"
                twheel.append(input(string))
            string="is " + str(twheel) + " correct Y/N\n"
            if "y" in input(string):                
                self.wheels = twheel
                print("Your wheels are " + str(self .wheels))
    
    def readSensors(self):
        lastVolume = self.soundVolume
        x,y = self.t.pos()
        self.temp=0
        for i in range(obs):
            objX = abs(Ox[i] - int(x))
            objY = abs(Ox[i] - int(y))
            objD = (objX**2 + objY**2)**0.5
            if objD < self.hRange:
                self.temp = 100
        
        disX = abs(Gx - int(x))
        disY = abs(Gy - int(y))
        dis = (disX**2 + disY**2)**0.5
        if dis < self.sRange:
            self.soundVolume = self.sRange - dis
        else:
            self.soundVolume = 0
        self.soundChange = self.soundVolume - lastVolume
    
    def move(self, direction):
        if direction == "F":
            self.t.forward(10)
        if direction == "B":
            self.t.forward(-10)
        if direction == "R":
            self.t.right(45)
            self.t.forward(10)
        if direction == "L":
            self.t.left(45)
            self.t.forward(10)
    
    def forward(self):
        return "F"
    def back(self):
        return "B"
    def left(self):
        return "R"
    def right(self):
        return "L"
    
    def intTimer(self):
        if self.timer < self.timerlength:
            self.timer+=1
        else:
            self.timer=0
    
    def avoidObject(self):
        self.timerlength = 10
        self.timer = 0
        while self.timer < self.timerlength:
            self.readSensors()
            if self.timer < 7:
                self.move(self.back())
            elif self.timer < 10:
                self.move(self.left())
            self.intTimer()
            time.sleep(sleepy)
    
    def followSound(self):
        self.timerlength = 10
        self.timer = 0
        while self.timer < self.timerlength and self.state == 1:
            self.readSensors()
            if self.temp > self.tempThreshold:
                state = 0
            elif self.soundChange > 0:
                self.move(self.forward())
            else:
                self.move(self.right())
            self.intTimer()
    
    def setState(self):
        if self.temp > 10:
            self.state = 0
        elif self.soundVolume > 0:
            self.state = 1
        else:
            self.state = 2
            
    def randomWalk(self, A,B,C,D):
        choice = ['F','B','L','R',]
        weight = [A,B,C,D]
        self.move(random.choices(choice,weight)[0])
        time.sleep(sleepy)
    
    def main(self):
        while True:
            self.readSensors()
            self.setState()
            if self.state == 0:
                self.avoidObject()
            elif self.state == 1:
                self.followSound()
            elif self.state == 2:
                self.randomWalk(10,0,2,2)
#behaviour design aim
#An increasing spiral with the aim to have the turtle travel a path that has a range of hearing that slightly overlaps
#the previous loops (to compensate for object avoidance). In the event of object avoidance, remember distance from centre
#move around obstacle, moving towards middle, before moving away from centre towards same distance and resuming along route
#Must track if route is similar enough
#Use angle (0* being north) and distance from centre. Tan^-1(Opp/Adj). Use different calculations depending on if X or Y is positive, and if X>Y, Y>X or Y=X
#As angle to turn will decrease with time, function will be? x^a? x^-a? etc etc
x = robot(wheels)
#x.checkWheels()
x.main()