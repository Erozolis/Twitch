import socket
import re
from settings import PREPEND, POSTPEND, SOCKETNUM, CHANNEL
from DBInteraction import assignPoints

def sendMessage(s, message):
    s.send(PREPEND + message + POSTPEND)
    
def readResponse(s):
    buffer = s.recv(SOCKETNUM)
    return buffer
    
def grabUser(response):
    return(response.split(':')[1].split('!')[0])
    
def parseMessage(response):
    return(response.split(CHANNEL + " :",1))
    
def chatAction(s, message, comparison, textResponse):
    m=comparison.search(message)
    if (m != None):
        if textResponse != "action only":
            sendMessage(s, textResponse)
        return True
    else:
        return False