# Copyright (c) 2008 Louai Al-Khanji

modules = dict()

def action(connection, sender, sender_ident, receiver, message):
    plain = message.split()[0].lower().lstrip("!")
    for key in keywords:
        if key.lower().startswith(plain):
            keywords[key](connection, sender, sender_ident, receiver, message)
            return

def load_module(connection, sender, sender_ident, receiver, message):
    try:
        msg = message.split()
        module = msg[1]
        mod = __import__(module)
        modules[module] = mod
        command = mod.info["command"]
        cb = mod.info["callback"]
        keywords[command] = cb
        
        connection.send_private_message(receiver,
                                        "Loaded module %s" % module)
    except Exception, e:
        connection.send_private_message(receiver,
                                        "Error loading module: %s" % str(e))

def delete_module(connection, sender, sender_ident, receiver, message):
    try:
        msg = message.split()
        module = msg[1]
        del keywords[module]
        del modules[module]
        connection.send_private_message(receiver,
                                        "Deleted module %s" % module)
    except Exception, e:
        connection.send_private_message(receiver,
                                        "Error deleting module: %s" %
                                        str(e))

def list_actions(connection, sender, sender_ident, receiver, message):
    connection.send_private_message(receiver, "Defined actions:");
    for x in keywords:
        connection.send_private_message(receiver, "%s" % x)

keywords = {
    "load": load_module,
    "delete": delete_module,
    "actions": list_actions
}
