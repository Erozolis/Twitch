import socket 
from settings import CHANNEL, HOST, PORT, IDENT, PASS

def openSocket():
#Define Constants

    s = socket.socket( ) #Create a socket
    s.connect((HOST, PORT)) #Connect to Twitch.tv
    s.send("PASS %s\r\n" % PASS) #Sends password
    s.send("NICK %s\r\n" % IDENT) #sends username
    s.send("USER %s %s \r\n" % (IDENT, HOST)) #signs in
    s.send("JOIN %s\r\n" % CHANNEL) #Joins channel chat
    return s