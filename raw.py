# Copyright (c) 2008 Teemu Rytilahti

from urllib import urlopen
import re
import random
import actions

def raw(connection, sender, sender_ident, receiver, message):
    msg = " ".join(message[1:])
    connection.write(msg)
    #recipient = actions.reply_to(connection, sender, receiver)
    #connection.send_private_message(recipient, response)
    
info = {
    "author": "Teemu Rytilahti",
    "command": "raw",
    "callback": raw,
    "permission": "overlord"
}
