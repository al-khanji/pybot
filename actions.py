# Copyright (c) 2008 Louai Al-Khanji

import users

modules = dict()

DEFAULT_QUIT_MSG = "My master bade me \"Quit thy lurking!\""
ACTION_CHAR = "!"

class ApplicationExitRequest(Exception):
    pass

def reply_to(connection, sender, receiver):
    if receiver == connection.nick:
        return sender
    else:
        return receiver

def action(connection, sender, sender_ident, receiver, message):
    if not message.startswith(ACTION_CHAR):
        return

    ident, host = sender_ident.split("@")
    user = users.find_user(sender, ident, host)

    words = message.split()
    plain = words[0].lower().lstrip(ACTION_CHAR)
    for key in keywords:
        if key.lower().startswith(plain):
            keys = keywords[key]
            if users.has_permission(user, keys["permission"]):
                call = keys["callback"]
                call(connection, sender, sender_ident, receiver, words)
                break

def load_module(connection, sender, sender_ident, receiver, words):
    if len(words) > 1:
        module = words[1]
        try:
            mod = __import__(module)
            modules[module] = mod
            command = mod.info["command"]
            keywords[command] = mod.info
            
            message = "Loaded module %s" % module
        except Exception, e:
            message = "Error loading module: %s" % str(e)
    else:
        message = "Specify module to load"

    recipient = reply_to(connection, sender, receiver)
    connection.send_private_message(recipient, message)

def delete_module(connection, sender, sender_ident, receiver, words):
    if len(words) > 1:
        module = words[1]
        try:
            del keywords[module]
            del modules[module]
            message = "Deleted module %s" % module
        except Exception, e:
            message =  "Error deleting module: %s" % str(e)
    else:
        message = "Specify module to unload"

    recipient = reply_to(connection, sender, receiver)
    connection.send_private_message(recipient, message)

def list_actions(connection, sender, sender_ident, receiver, words):
    recipient = reply_to(connection, sender, receiver)
    connection.send_private_message(recipient, "Defined actions:");
    for key in keywords:
        connection.send_private_message(recipient, key)

def quit(connection, sender, sender_ident, receiver, words):
    raise ApplicationExitRequest, DEFAULT_QUIT_MSG

keywords = {
    "load": { "callback": load_module, "permission": "overlord" },
    "delete": { "callback": delete_module, "permission": "overlord" },
    "actions": { "callback": list_actions, "permission": "public" },
    "quit": { "callback": quit, "permission": "overlord" }
}
