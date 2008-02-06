def get_time(*args, **keys):
    import time
    return time.strftime("%Y-%m-%d-%H-%M-%S")

def get_uniresta(msg):
    import uniresta
    return uniresta.uniresta(msg)

def match(act):
    plain = act.split()[0].lower().lstrip("!")
    for key in keywords:
        if key.lower().startswith(plain):
            return True
    return False

def action(act):
    plain = act.split()[0].lower().lstrip("!")
    for key in keywords:
        if key.lower().startswith(plain):
            return keywords[key](act)

keywords = {
    "aika": get_time,
    "uniresta": get_uniresta
}
