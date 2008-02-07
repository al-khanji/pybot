# Copyright (c) 2008 Louai Al-Khanji

import uniresta

def do_uniresta(*args, **keys):
    return uniresta.uniresta(*args, **keys)

def action(connection, sender, sender_ident, receiver, message):
    plain = message.split()[0].lower().lstrip("!")
    for key in keywords:
        if key.lower().startswith(plain):
            keywords[key](connection, sender, sender_ident, receiver, message)

keywords = {
    "uniresta": do_uniresta
}
