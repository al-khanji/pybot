# Copyright (c) 2008 Louai Al-Khanji

import config
import irc
import logging
import actions

def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    connections = set()

    for network in config.networks:
        try:
            connection = irc.Connection(network)
            connection.connect()
            connections.add(connection)
        except irc.ConnectionError, e:
            logging.error("Error connecting to %s -> %s" %
                          (network["server"], e))
            logging.info("Removing from connections.")

    while True:
        done = set()
        for c in connections:
            if c.done is True:
                done.add(c)
        connections -= done

        if len(connections) == 0:
            logging.info("No connections left.")
            break

        try:
            irc.process_connections(connections)
        except actions.ApplicationExitRequest, msg:
            logging.info("Exit requested, closing remaining connections")
            for connection in connections:
                connection.quit(msg)

    logging.info("All done.")

if __name__ == "__main__":
    main()
