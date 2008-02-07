# -*- coding: iso-8859-1 -*-

# This particular file is public domain

defaults = {
    "nick": "slougibot",
    "realname": "minä olen botti",
    "port": 6667,
    "mode": 0, # 8 = +i, 4 = +w, 12 = +wi
    "ssl": False,
    "channels": [],
    "quit_message": "My master bade me \"Quit thy lurking!\""
}

networks = [
    { "server": "irc.virtues.fi", "channels": ["#ouspg"], "ssl": True, "port": 994 }
]

# don't touch stuff below this line please

for network in networks:
    n = dict(defaults)
    n.update(network)
    network.update(n)
