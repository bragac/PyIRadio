import vlc
#Wraps current audio library in a helper class. Will allow for change in library
#in the future.
#Change depends on FFMPGA ctypes wrapping progress

#Need to do error checking for invalid stationURLS
class InternetRadio():

    def __init__(self):
        self.mediaPlayerInst = None
        self.curStation = "None"

    def setStation(self, stationURL, stationName):
        if (self.mediaPlayerInst == None):
            self.mediaPlayerInst = vlc.MediaPlayer(stationURL)
        else:
            self.mediaPlayerInst.stop()
            self.mediaPlayerInst.set_mrl(stationURL)
        self.curStation = stationName

    def setVolume(self, volume):
        if (self.mediaPlayerInst != None):
            self.mediaPlayerInst.audio_set_volume(volume)

    def getVolume(self):
        if (self.mediaPlayerInst != None):
            return self.mediaPlayerInst.audio_get_volume()

    def playStation(self):
        if (self.mediaPlayerInst != None):
            self.mediaPlayerInst.play()

    def stopStation(self):
        if (self.mediaPlayerInst != None):
            self.mediaPlayerInst.stop()

    def togglePause(self):
        if (self.mediaPlayerInst != None):
            self.mediaPlayerInst.pause()

    def muteStation(self):
        if (self.mediaPlayerInst != None):
            self.mediaPlayerInst.audio_toggle_mute()

    #Frees player resources
    def closePlayer(self):
        if (self.mediaPlayerInst != None):
            self.mediaPlayerInst.release()
            self.mediaPlayerInst = None

    #Currently only returns if the player is playing or not. No other info given
    def getPlayerState(self):
        if (self.mediaPlayerInst != None):
            return self.mediaPlayerInst.is_playing()
        else: return 0

if __name__ == "__main__":
    currentRadio = InternetRadio()
    currentRadio.setStation("http://allstream.rainwave.cc:8000/omniwave.mp3?1388431588515.mp3", "OCREMIX")
    currentRadio.playStation()
