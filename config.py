# -*- coding: iso-8859-1 -*-

# This particular file is public domain

defaults = {
    "nick": "slougibot",
    "realname": "min� olen botti",
    "port": 6667,
    "mode": 0, # 8 = +i, 4 = +w, 12 = +wi
    "ssl": False,
    "channels": []
}

networks = [
    { "server": "irc.cc.tut.fi", "channels": ["#devel-fi"] }
]

# don't touch stuff below this line please

for network in networks:
    n = dict(defaults)
    n.update(network)
    network.update(n)
