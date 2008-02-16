# Copyright (c) 2008 Louai Al-Khanji

#import uniresta
#import willab

#def do_uniresta(*args, **keys):
#    return uniresta.uniresta(*args, **keys)

#def do_willab(*args, **keys):
#    return willab.willab(*args, **keys)

def load_module(connection, sender, sender_ident, receiver, message):
    #if (sender_name != "teprrr")
    #    return
    
    msg = message.split()
    module = msg[1]
    
    mod = __import__(module)
    command = mod.info["command"]
    cb = mod.info["callback"]
    keywords[command] = cb
    
    connection.send_private_message(receiver, "Loaded module %s" % module)

def action(connection, sender, sender_ident, receiver, message):
    plain = message.split()[0].lower().lstrip("!")
    for key in keywords:
        if plain.lower().startswith(key):
            keywords[key](connection, sender, sender_ident, receiver, message)
            return

def list_modules(connection, sender, sender_ident, receiver, message):
    connection.send_private_message(receiver, "Available modules:");
    for x in keywords:
        connection.send_private_message(receiver, "%s" % x)

def delete_module(connection, sender, sender_ident, receiver, message):
    msg = message.split()
    module = msg[1]
    
    del keywords[module]
    #del module
    
    connection.send_private_message(receiver, "Deleted module %s" % module)

keywords = {
    "load": load_module,
    "delete": delete_module,
    "modules": list_modules
}