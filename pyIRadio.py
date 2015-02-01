import InternetRadio
import stationListParser
import time
import sys
class radioInterface():
    
    def __init__(self):
        self.radio = InternetRadio.InternetRadio()
        self.listParser = stationListParser.stationListParser("radiolist.txt")
        self.running = False
        self.muted = False
        self.stationName = ""
        #self.userPrompt()
        
    def userPrompt(self):
        endProgram = False
        print "Welcome to pyIRadio!" 
        print "Using this program you may play any internet radio station right on your desktop!"
        self.printStationNames()
        print "\nPlease type help for a list of commands\n" 
        while not endProgram:
            arguements = raw_input(">>> ").split(" ")
            command = arguements[0]
            if command == "help":
                self.helpPrompt()
            elif command == "play":
                if len(arguements) < 2:
                    print self.errorMessages(2)
                else:
                    self.radioPlay(arguements[1])
            elif command == "stop":
                self.radioStop()
            elif command == "pause":
                self.togglePause()
            elif command == "mute":
                self.toggleMute()
            elif command == "volume":
                if len(arguements) != 2:
                    print self.errorMessages(2)
                else:
                    self.changeVolume(int(arguements[1]))
            elif command == "stations":
                self.printStationNames()
            elif command == "add":
                if len(arguements) != 3:
                    print self.errorMessages(2)
                else:
                    self.addStation(arguements[1],arguements[2])
            elif command == "quit":
                endProgram  = True
                self.radioStop()
            else:
                print "Invalid Command. Please type help for a list of commands"
            
    def helpPrompt(self):
        print "What follows is a list of commands and their uses:"
        print "Command: help\nPurpose: Gives user a list of commands and their uses\n"
        print "Command: play <Station Name>\nPurpose: Searches the list of stations for the given station name. The corresponding station commences playing\n"
        print "Command: stop\nPurpose: Stops playback of the current station (if any)\n"
        print "Command: pause\nPurpose: Pauses playback of the current station. If the station is already paused this function resumes the playback\n"
        print "Command: mute\nPurpose: Turns playback volume to 0. If volume already at 0 volume is returned to its' previous value\n"
        print "Command: volume <value>\n Purpose: Sets playback volume to the given value. If value exceeds 100 the value defaults to 100\n"
        print "Command: stations\nPurpose: Prints out a list of station names stored in the saved stations file\n"
        print "Command: add <station URL> <station name>\nPurpose: Adds the given station URL/station name pair to the saved stations file\n"
        print "Command: quit\nPurpose: Quits the program\n"

    def radioPlay(self,stationName):
        tries = 0
        self.stationName = ""
        self.running = False
        stationURL= self.retrieveURL(stationName)
        if stationURL == "":
            print self.errorMessages(1)
            return -1
        #Make it grab the url from the list
        self.radio.setStation(stationURL,stationName)
        self.radio.playStation()
        #Ensure connection is made else error and cleanup
        print "Loading station..."
        while not self.radio.getPlayerState():
            if tries > 30:
                print self.errorMessages(0)
                self.radio.closePlayer()
                return -1
            else:
                tries +=1
                time.sleep(0.5)
        self.stationName = stationName
        print "\nCurrently playing %s. Volume level set at %d."%(stationName,self.radio.getVolume())
        self.running = True
        return 0
        
    def togglePause(self):
        if self.running:
            self.radio.togglePause()
            if self.radio.getPlayerState(): print "Pausing %s"%(self.stationName)
            else: print "Resuming %s"%(self.stationName)

    def radioStop(self):
        self.radio.stopStation()
        self.radio.closePlayer()
        print "Stopping %s"%(self.stationName)

    #Not working
    def changeVolume(self, newVol):
        self.radio.setVolume(newVol)
        print "Volume set to %s"%(newVol)

    def toggleMute(self):
        if self.muted:
            print "Radio has been unmuted"
            self.muted = False
        else:
            print "Radio has been muted"
            self.muted = True
        self.radio.muteStation()

    def printStationNames(self):
        print "The currently saved stations are:"
        for station in self.listParser.parseURLsAndNames():
            print station[1]

    #Helper function. Not invoked through a user command.
    def retrieveURL(self,stationName):
        #Automatically used current version of file instead of stored list
        matchingStations = self.listParser.searchStationList(stationName)
        if len(matchingStations) ==0:
            return ""
        elif len(matchingStations) == 1:
            return matchingStations[0][0]
        else:
            print "Multiple stations found: \n"
            for results in matchingStations:
                print results[0]
            try:
                choice = input("\nPlease enter a number between 1 and %d to choose a station: "%(len(matchingStations)))
                return matchingStations[choice-1][0]
            except:
                print "You entered an invalid choice"
                return ""
                


    def addStation(self,stationURL,stationName):
        if self.listParser.searchStationList(stationURL):
            print "Station URL already exists. No need to add provided station"
        elif self.listParser.searchStationList(stationName):
            print "Station Name already in use. Please choose another"
        else:
            self.listParset.addStation(stationURL,stationName)

    #Helper function. Not invoked through a user command
    def errorMessages(self,errorVal):
        return { 0: "ERORR: Issue loading station url provided",
                 1: "ERROR: No station matching name provided",
                 2: "ERROR: Incorrect number of arguements"}.get(errorVal)
        
    

            
        
    
if __name__ == "__main__":
    controller = radioInterface()
    controller.userPrompt()
    sys.stderr.close()
    
