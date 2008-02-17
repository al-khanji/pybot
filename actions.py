# Copyright (c) 2008 Louai Al-Khanji

modules = dict()

DEFAULT_QUIT_MSG = "My master bade me \"Quit thy lurking!\""
ACTION_CHAR = "!"

class ApplicationExitRequest(Exception):
    pass

def reply_to(connection, sender, receiver):
    return sender if (receiver == connection.nick) else receiver

def action(connection, sender, sender_ident, receiver, message):
    if not message.startswith(ACTION_CHAR):
        return

    words = message.split()
    plain = words[0].lower().lstrip(ACTION_CHAR)
    for key in keywords:
        if key.lower().startswith(plain):
            keywords[key](connection, sender, sender_ident, receiver,
                          words)
            return

def load_module(connection, sender, sender_ident, receiver, words):
    if len(words) > 1:
        module = words[1]
        try:
            mod = __import__(module)
            modules[module] = mod
            command = mod.info["command"]
            cb = mod.info["callback"]
            keywords[command] = cb
            
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
    if sender in ["slougi", "teprrr"]:
        raise ApplicationExitRequest, DEFAULT_QUIT_MSG

keywords = {
    "load": load_module,
    "delete": delete_module,
    "actions": list_actions,
    "quit": quit
}
