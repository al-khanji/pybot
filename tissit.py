# Copyright (c) 2008 Teemu Rytilahti

from urllib import urlopen
import re
import random
import actions

BASE_URL = "http://www.heinola.org/~count/tissit/"

def tissit(connection, sender, sender_ident, receiver, message):
    response = str()
    
    html = urlopen(BASE_URL)
    
    p = re.compile('<A HREF="(.+?\.jpg)">')

    imagelist = p.findall(html.read())
    
    num = random.randint(0, len(imagelist))
    
    response = 'Tissit: %s%s' % (BASE_URL, imagelist[num])
    
    recipient = actions.reply_to(connection, sender, receiver)
    connection.send_private_message(recipient, response)
    
info = {
    "author": "Teemu Rytilahti",
    "command": "tissit",
    "callback": tissit,
    "permission": "public"
}
