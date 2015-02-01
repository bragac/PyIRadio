
class stationListParser():

    def __init__(self, stationFile):
        self.file = stationFile

    def changeFile(self, stationFile):
        self.file = stationFile
        
    def parseNames(self):
        myFile = open(self.file)
        stationNames = []
        for station in myFile:
            stationNames.append(station.split(",")[1].strip(""))
        myFile.close()
        return stationNames

    def parseURL(self):
        myFile = open(self.file)
        stationURLs = []
        for station in myFile:
            stationURLs.append(station.split(",")[1].strip())
        myFile.close()
        return stationURLs

    def parseURLsAndNames(self):
        myFile = open(self.file)
        contents = []
        for station in myFile:
            contents.append(station.strip().split(","))
        myFile.close()
        return contents

    def addStation(self, stationURL, stationName):
        myFile = open(self.file,"a")
        myFile.write(stationURL +","+stationName)
        myFile.close()

    #Removes any stations containing the stationIdentifier
    def removeStation(self, stationIdentifier):
        myFile = open(self.file)
        stationString = ""
        for station in myFile:
            if station.find(stationIdentifier):
                stationString = stationString + station.strip() +"\n"
        myFile.close()
        myFile = open(self.file,"w")
        myFile.write(stationString.strip())
        myFile.close()


    def searchStationList(self,keyword):
        myFile = open(self.file)
        matchingStations = []
        for station in myFile:
            if station.find(keyword)!= -1:
                matchingStations.append(station.strip().split(","))
        return matchingStations
