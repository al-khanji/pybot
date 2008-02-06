import config
import irc

def main():
    connections = list()

    for network in config.networks:
        connection = irc.Connection(network)
        connections.append(connection)

    while irc.quit is False:
        irc.do_connections(connections)

    for connection in connections:
        connection.quit(irc.quit)

if __name__ == "__main__":
    main()