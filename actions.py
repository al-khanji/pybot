# Copyright (c) 2008 Louai Al-Khanji

modules = dict()

def load_module(connection, sender, sender_ident, receiver, message):
    msg = message.split()
    module = msg[1]

    try:
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

def action(connection, sender, sender_ident, receiver, message):
    plain = message.split()[0].lower().lstrip("!")
    for key in keywords:
        if key.lower().startswith(plain):
            keywords[key](connection, sender, sender_ident, receiver, message)
            return

def list_modules(connection, sender, sender_ident, receiver, message):
    connection.send_private_message(receiver, "Available modules:");
    for x in keywords:
        connection.send_private_message(receiver, "%s" % x)

def delete_module(connection, sender, sender_ident, receiver, message):
    msg = message.split()
    module = msg[1]

    try:
        del keywords[module]
        del modules[module]
        connection.send_private_message(receiver,
                                        "Deleted module %s" % module)
    except Exception, e:
        connection.send_private_message(receiver,
                                        "Error deleting module: %s" %
                                        str(e))

keywords = {
    "load": load_module,
    "delete": delete_module,
    "modules": list_modules
}
