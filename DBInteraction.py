import MySQLdb
import re
from settings import DBLOCATION, DBUSER, DBPASS, DBNAME
db = MySQLdb.connect(DBLOCATION, DBUSER, DBPASS, DBNAME)
cursor = db.cursor()

def register(username, message):
    try:
        m=re.compile(r'#register (?P<ign>\w+)')
        j=m.search(message)
        ign = j.group('ign')
        query = "INSERT INTO user (name, ign) VALUES ('" + username+ "', '" + ign +"')"
    except:
        submission = "incorrect formatting"
        return submission
    try:
        result = cursor.execute(query)
        db.commit()
        submission = "Successfully submitted username"
    except:
        query = "UPDATE user SET name= '" + username + "', ign = '" + ign +"' where name = '" + username + "'"
        result = cursor.execute(query)
        db.commit()
        submission = "Successfully modified username"
    return submission
    
def assignPoints(message):
    r = re.compile(r'#addPoints (?P<username>\w+) (?P<points>\w+)$', re.IGNORECASE)
    m = r.search(message)
    points = m.group('points')
    username = m.group('username')
    print points
    print username
    query = "UPDATE user set points=points+" + points + " where name='" + username + "'"
    print query
    try:
        result = cursor.execute(query)
        db.commit()
        print "got here"
        query = "SELECT points FROM user where name='" + username + "'"
        print query
        result = cursor.execute(query)
        totalPoints = cursor.fetchone()[0]
        submission = username + " now has " + str(totalPoints) + " points."
    except:
        submission = "Error updating points. This user may not have registered"
    return submission
def isRegistered(username):
    query = "SELECT is_registered FROM user where name = '" + username + "'"
    cursor.execute(query)
    try:
        if(cursor.fetchone()[0] == 1):
            return True
        else:
            return False
    except:
        return False