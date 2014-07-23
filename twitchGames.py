import socket
import random 

def scramble(message):
    word = list(message)
    return (''.join(random.sample(word,len(word))))
    
