# Copyright (c) 2008 Louai Al-Khanji

import config
import irc

def main():
    connections = list()

    for network in config.networks:
        try:
            connection = irc.Connection(network)
            connection.connect()
            connections.append(connection)
        except irc.ConnectionError:
            print "Error connecting to %s, removing from connection list" \
                   % network["server"]

    while irc.quit is False and len(connections) != 0:
        irc.do_connections(connections)

    if irc.quit is not False:
        print "Quit requested, closing remaining connections"
        for connection in connections:
            connection.quit()

    if len(connections) == 0:
        print "No connections left, all done here."

if __name__ == "__main__":
    main()
