import config
import irc

def main():
    connections = list()

    for network in config.networks:
        try:
            connection = irc.Connection(network)
            connection.connect()
            connection.join_channels()
            connections.append(connection)
        except irc.ConnectionError:
            print "Error connecting to %s, removing from connection list" \
                   % network["server"]

    while irc.quit is False:
        irc.do_connections(connections)

    for connection in connections:
        connection.quit(irc.quit)

if __name__ == "__main__":
    main()