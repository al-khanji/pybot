# Copyright (c) 2008 Teemu Rytilahti

from urllib import urlopen
import xml.dom.minidom

BASE_URL = "http://weather.willab.fi/weather.xml"

# location and precipitation values are also available, but can't be parsed like this..
data_available = "time", "tempnow", "temphi", "templo", "dewpoint", "humidity", "airpressure", "windspeed", "windspeedmax", "winddir", "solarrad"

#def main():
#    willab()

def read_tag(doc, tag_name):
    element = doc.getElementsByTagName(tag_name)[0]
    value = element.firstChild.toxml()
    unit = element.getAttribute("unit")
    
    return value, unit

#def willab():
def willab(connection, sender, sender_ident, receiver, message):
    response = str()
    
    html = urlopen(BASE_URL)
    
    content = xml.dom.minidom.parse(html)
    
    data = dict()
    for x in data_available:
        data[x] = read_tag(content, x)
     
    time = data["time"][0]
    temp = "%s %s" % data["tempnow"]
    airpressure = "%s %s" % data["airpressure"]
    windspeed = "%s %s" % data["windspeed"]
    
    response = 'Linnanmaa: %s, %s, %s (%s)' % (temp, windspeed, airpressure, time)
    
    if receiver == connection.nick:
        connection.send_private_message(sender, response)
    else:
        connection.send_private_message(receiver, response)
    
info = {
    "author": "Teemu Rytilahti",
    "command": "linnanmaa",
    "callback": willab
}
