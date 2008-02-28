# Copyright (c) 2008 Teemu Rytilahti

from urllib import urlopen
import re
import random
import actions

BASE_URL = "http://www.heinola.org/~count/tissit/"

html = urlopen(BASE_URL)
p = re.compile('<A HREF="(.+?\.jpg)">')
IMAGELIST = p.findall(html.read())


def tissit(connection, sender, sender_ident, receiver, message):
    global IMAGELIST

    num = random.randint(0, len(IMAGELIST))    
    response = 'Tissit: %s%s' % (BASE_URL, IMAGELIST[num])

    recipient = actions.reply_to(connection, sender, receiver)
    connection.send_private_message(recipient, response)
    
info = {
    "author": "Teemu Rytilahti",
    "command": "tissit",
    "callback": tissit,
    "permission": "public"
}
