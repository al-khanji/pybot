# Copyright (c) 2008 Louai Al-Khanji

import os
import csv

PERMISSIONS = ["public", "overlord"]

CONFIG_HOME = os.path.join(os.path.expanduser("~"), ".pybot")
if not os.path.lexists(CONFIG_HOME):
    os.mkdir(CONFIG_HOME)

USERDB = os.path.join(CONFIG_HOME, "users.csv")
CSV_FIELDS = ("nick", "ident", "host", "permission")
csv.register_dialect('pybot', delimiter=':', quoting=csv.QUOTE_NONE)

def _write_initial_config():
    if os.path.lexists(USERDB):
        return
    userdb = open(USERDB, "wb")
    writer = csv.DictWriter(userdb, fieldnames=CSV_FIELDS, dialect="pybot")
    slougi = { "nick": "slougi",
               "ident": "~louaialk",
               "host": "tuomi.oulu.fi",
               "permission": PERMISSIONS[-1] }
    writer.writerow(slougi)
    del writer
    userdb.close()
_write_initial_config()

def has_permission(user, required_permission):
    if user is not None:
        user_index = PERMISSIONS.index(user["permission"])
    else:
        user_index = 0
    permission_index = PERMISSIONS.index(required_permission)
    return user_index >= permission_index

def find_user(nick, ident, host):
    result = None
    userdb = open(USERDB, "rb")
    reader = csv.DictReader(userdb, fieldnames=CSV_FIELDS, dialect="pybot")
    for user in reader:
        if user["nick"] == nick \
        and user["ident"] == ident \
        and user["host"] == host:
            result = user
            break
    userdb.close()
    return result

