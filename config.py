# -*- coding: iso-8859-1 -*-

defaults = {
    "nick": "slougibot",
    "realname": "minä olen botti",
    "port": 6667,
    "mode": 0,
    "ssl": False
}

networks = [
    #{ "server": "irc.cs.tut.fi", "channels": ["#toimisto.org"] }
    { "server": "irc.virtues.fi",
      "channels": ["#clarinet"],
      "port": 994,
      "ssl": True }
]

# don't touch stuff below this line please

for network in networks:
    n = dict(defaults)
    n.update(network)
    network.update(n)
