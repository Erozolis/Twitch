import socket #Imports socket for communicating with the server
import time
import winsound
import MySQLdb
import re
import pyttsx
#import webbrowser
from DBInteraction import register, assignPoints, isRegistered
from SocketCreate import openSocket
from settings import PREPEND, POSTPEND, DBLOCATION, DBUSER, DBPASS, DBNAME
from twitchInteraction import sendMessage, readResponse, grabUser, parseMessage, chatAction
from twitchGames import scramble

db = MySQLdb.connect(DBLOCATION, DBUSER, DBPASS, DBNAME)
cursor = db.cursor()
engine=pyttsx.init()
engine.setProperty('rate', 120)
engine.setProperty('volume', 1.0)
engine.setProperty('age', 30)
engine.setProperty('id', 2)
s = openSocket()
lastbeeped = time.time()-300
while (1):
    response = readResponse(s)
    user = grabUser(response)
    # user=response.split(':')[1] #Split the the response using a : as the delimiter and assign the string at index 1
    # user = user.split('!')[0] #Split the string using a ! as the delimiter and assign the string at index 0
    action = response.split('#')[0].split(' ')[1]
    if (response.find("PING") != -1):
        s.send(response.replace("PING", "PONG"))
    if (action.find("JOIN") != -1):
        respond = "Welcome to the stream " + user + "!"
        engine.say("Welcome " + user)
        engine.runAndWait()
        s.send(PREPEND + respond + POSTPEND)
    if (action.find("PART") != -1):
        respond = user + " has left the stream."
        s.send(PREPEND + respond + POSTPEND)
    message=parseMessage(response)
    if len(message)>1: #Checks to see if something was typed in chat
        message = message[1].split(POSTPEND)[0] #Converts the message into a string
        print message
        if (message.startswith('%')):
            if (isRegistered(user)):
                engine.say(message.replace('%', ''))
                engine.runAndWait()
            else:
                sendMessage(s, "You are not registered to use the text to speech functionality")
        result = chatAction(s, message, re.compile(r'\b(hi|hello)\b', re.IGNORECASE), "Hello " + user + "!")
        result = chatAction(s, message, re.compile(r'#lolking', re.IGNORECASE), """\
        I have 2 accounts: \
        MisterMrErik: http://www.lolking.net/summoner/na/30425542 \
        Nidalee Sucks: http://www.lolking.net/summoner/na/47443725""")
        result = chatAction(s, message, re.compile(r'#currentgame', re.IGNORECASE), "Here is my current game: http://www.lolnexus.com/NA/search?name=mistermrerik&region=NA")
        result = chatAction(s, message, re.compile(r'#register', re.IGNORECASE), "action only")
        if(result == True ):
            sendMessage(s,register(user, message))
        if (user == "mistermrerik"):
            result = chatAction(s, message, re.compile(r'#addPoints', re.IGNORECASE), "action only")
            if (result == True):
                sendMessage(s, assignPoints(message))
