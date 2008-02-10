# Copyright (c) 2008 Louai Al-Khanji

import config
import irc
import logging

def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    connections = list()

    for network in config.networks:
        try:
            connection = irc.Connection(network)
            connection.connect()
            connections.append(connection)
        except irc.ConnectionError, e:
            logging.error("Error connecting to %s -> %s" % (network["server"], e))
            logging.info("Removing from connections.")

    while irc.quit is False and len(connections) != 0:
        irc.do_connections(connections)

    if irc.quit is not False:
        logging.info("Quit requested, closing remaining connections")
        for connection in connections:
            connection.quit()
    if len(connections) == 0:
        logging.info("No connections left.")
    logging.info("All done.")

if __name__ == "__main__":
    main()
