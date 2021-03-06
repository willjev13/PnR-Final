import pigo
import time
import random

'''
MR. A's Final Project Student Helper
'''

class GoPiggy(pigo.Pigo):

    ########################
    ### CONTSTRUCTOR - this special method auto-runs when we instantiate a class
    #### (your constructor lasted about 9 months)
    ########################

    def __init__(self):
        print("Your piggy has be instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 110
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.STOP_DIST = 35
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 50
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 50
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.menu()


    ########################
    ### CLASS METHODS - these are the actions that your object can run
    #### (they can take parameters can return stuff to you, too)
    #### (they all take self as a param because they're not static methods)
    ########################


    ##### DISPLAY THE MENU, CALL METHODS BASED ON RESPONSE
    def menu(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "c": ("Calibrate", self.calibrate),
                "t": ("Turn test", self.turn_test),
                "s": ("Check status", self.status),
                "q": ("Quit", quit),
                "f": ("Final", self.final),
                "o": ("Count obstacles", self.count_obstacles),
                "a": ("Total obstacles", self.total_obstacles),
                "z": ("Sniff opening", self.sniff_opening),
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def count_obstacles(self):
        # run a scan
        self.wide_scan()
        # count how many obstacles I've found
        counter = 0
        # starting state assumes no obstacle
        found_something = False
        # loop through all my scan data
        for x in self.scan:
            # if x is not None and really close
            if x and x < self.STOP_DIST:
                # if I've already found something
                if found_something:
                    print("obstacle continues")
                # if this is a new obstacle
                else:
                    # switch my tracker
                    found_something = True
                    print("start of a new obstacle")
                    # if my data show safe spaces...
            if x and x > self.STOP_DIST:
                # if my tracker has been triggered
                if found_something:
                    print("end of obstacle")
                    # reset tracker
                    found_something= False
                    # increase count of obstacles
                    counter += 1
        print("Total number of obstacles in this scan: " + str(counter))
        return counter

    def final(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"
        while True:
            if self.is_clear():
                self.cruise()
            answer = self.choose_path()
            print("My choose_path method told me to turn: " + answer)
            if answer == "left":
                self.encL(4)
                self.maneuver()
            elif answer == "right":
                self.encR(4)
                self.maneuver()
            # wish to stop after 10 and rescan, work to the edge of obstacle and then cruise

        #want to add to maneuver way to go towards the greatest possible distance reading, not average
        #scan and if distance >150 is found, immediately go that way
        #worked with mr. A on sniff opening
    def maneuver(self):
        print("My turn_track is: " + str(self.turn_track))
        if self.turn_track > 0:
            while self.is_clear():
                self.encF(8)
            self.servo(self.MIDPOINT + 25)
            if self.dist() > self.STOP_DIST + 20:
                time.sleep(.1)
                self.restore_heading()
                return
            self.servo(self.MIDPOINT)



        # DECIDE WHICH WAY TO TURN
        #discussed a way to identify and slowly turn to the largest gap with Mr. A, spent 15 minutes at the end of class developing code below
    def sniff_opening(self):
            print('Doing my full scan')
            self.wide_scan()
            print('Finding the largest result')
            largest = 0
            for x in range(170):
                if self.scan[x] > largest:
                    largest = x
                    print("My current largest value is: " + str(self.scan[x]) + " at degree" + str(x))
            # TODO: Start turning toward the best angle once the above loop finishes
            self.servo(self.MIDPOINT)
            if largest > self.MIDPOINT:
                while abs(self.dist() - largest) > 10:
                    self.encR(3)
            elif largest < self.MIDPOINT:
                while abs(self.dist() - largest) > 10:
                    self.encL(3)

    #if encR, servo sweep from center to left limit
    #if encL, servo sweep from center to right limit
    #if total_obstacles are greater than 0, encF(5) and servo sweep
    #else reset turn track to 0, cruise

    def cruise(self):
        self.fwd()  # I added this to pigo
        while self.is_clear():
            time.sleep(.1)
        self.stop()
        self.encB(3)

    def total_obstacles(self):
        counter = 0
        for x in range(4):
            counter += self.count_obstacles()
            self.encR(6)
        print("Total number of obstacles found on this scan: " + str(counter))


    def turn_test(self):
        while True:
            ans = raw_input('Turn right, left or stop? (r/l/s): ')
            if ans == 'r':
                val = int(raw_input('/nBy how much?: '))
                self.encR(val)
            elif ans == 'l':
                val = int(raw_input('/nBy how much?: '))
                self.encL(val)
            else:
                break
        self.restore_heading()

    def restore_heading (self):
        print("Now I'll turn back to starting position")
        if self.turn_track > 0:
            val = self.turn_track
            self.encL(val)
        elif self.turn_track < 0:
            val = abs(self.turn_track)
            self.encR(val)




    def sweep(self):
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, 2):
            self.servo(x)
            self.scan[x] = self.dist()
        print("Here's what I saw: ")
        print(self.scan)

    def safety_dance(self):
        for y in range(3):
            for x in range(self.MIDPOINT - 60,self.MIDPOINT + 60,2):
                self.servo(x)
                if self.dist() <15:
                    print("Houston, we have a problem!")
                    return
            self.encR(4)
        self.dance()

    #YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        self.search_and_destroy()
        self.squaredance()
        self.douggie()
        self.dosey_doe()
        self.douggie()

    def search_and_destroy(self):
        print('Search and Destroy')
        for x in range(3):
            self.servo(30)
            self.encR(3)
            self.servo(140)
            self.encL(3)

    def squaredance(self):
        print ('Squaredance')
        self.encF(30)
        self.encR(29)
        time.sleep(.25)
        self.encR(6)
        time.sleep(.25)
        self.encF(30)
        self.encR(29)
        time.sleep(.25)
        self.encR(6)
        time.sleep(.25)
        self.encF(30)
        self.encR(29)
        time.sleep(.25)
        self.encR(6)
        self.encF(30)
        time.sleep(.2)

    def douggie(self):
        print('Douggie')
        time.sleep(.1)
        self.encB(10)
        self.encR(3)
        self.servo(80)
        time.sleep(.1)
        self.encL(6)
        self.servo(80)
        time.sleep(.1)
        self.encR(3)

    def dosey_doe(self):
        print ('Dosey Doe')
        self.encR(72)
        time.sleep(.05)
        self.encL(70)
        self.encF(5)
        self.encB(5)
        self.servo(30)
        self.servo(150)

    def douggie(self):
        print ('Douggie')
        self.encB(10)
        self.encR(3)
        self.servo(80)
        time.sleep(.1)
        self.encL(6)
        self.servo(80)
        time.sleep(.1)
        self.encR(3)





    ########################
    ### MAIN LOGIC LOOP - the core algorithm of my navigation
    ### (kind of a big deal)
    ########################

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("[ Press CTRL + C to stop me, then run stop.py ]\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        # this is the loop part of the "main logic loop"

    def encR(self, enc):
        pigo.Pigo.encR(self, enc)
        self.turn_track += enc

    def encL(self, enc):
        pigo.Pigo.encL(self, enc)
        self.turn_track -= enc



####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit

##################################################################
######## The app starts right here when we instantiate our GoPiggy

try:
    g = GoPiggy()
except (KeyboardInterrupt, SystemExit):
    from gopigo import *
    stop()