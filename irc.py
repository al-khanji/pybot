# Copyright (c) 2008 Louai Al-Khanji

import socket
import logging
import select
import actions

BUFSIZE = 4096
MAX_MSG = 420 # conservative length, depends on irc server
LINE_BREAK = "\r\n"

# Constants
NUMERIC_REPLY_MIN = 1
NUMERIC_REPLY_MAX = 399
ERROR_MIN = 400
ERROR_MAX = 599

# Numeric replies

RPL_MYINFO = 4

class error(Exception):
    pass

class ConnectionError(Exception):
    pass

class Connection(object):
    def __init__(self, params):
        self.__dict__.update(params)
        self._leftover = ""
        self.socket = None
        self.done = False

    def fileno(self):
        return self.socket.fileno()

    def write(self, message):
        logging.info("<<< " + repr(message))
        if self.ssl:
            self.ssl.write("%s%s" % (message, LINE_BREAK))
        else:
            self.socket.sendall("%s%s" % (message, LINE_BREAK))

    def connect(self):
        try:
            for res in socket.getaddrinfo(self.server,
                                           self.port,
                                           socket.AF_UNSPEC,
                                           socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    self.socket = socket.socket(af, socktype, proto)
                except socket.error:
                    self.socket = None
                    continue
                try:
                    self.socket.connect(sa)
                except:
                    self.socket.close()
                    self.socket = None
                    continue
                break
            if self.socket is None:
                raise ConnectionError, "could not open socket"
            if self.ssl:
                self.ssl = socket.ssl(self.socket)
        except socket.gaierror, e:
            raise ConnectionError, e

        self.write("NICK %s" % self.nick)
        self.write("USER %s %s dummy :%s" %
                   (self.nick, self.mode, self.realname))

    def join_all_channels(self):
        self.write("JOIN %s" % ",".join(self.channels))

    def process(self):
        if self.ssl:
            data = self._leftover + self.ssl.read()
        else:
            data = self._leftover + self.socket.recv(BUFSIZE)

        lines = data.split(LINE_BREAK)
        if not data.endswith(LINE_BREAK):
            self._leftover = lines.pop(-1)
        else:
            self._leftover = ""

        for line in lines:
            self.parse_line(line)

    def parse_line(self, line):
        line = line.strip()
        if len(line) is 0:
            return

        logging.info(">>> " + repr(line))

        words = line.split()
        message = " ".join(words[3:]).lstrip(":")

        if line.startswith(":"):
            try:
                # numeric
                code = int(words[1])
                if code >= NUMERIC_REPLY_MIN and code <= NUMERIC_REPLY_MAX:
                    self.handle_numeric_reply(code, message)
                elif code >= ERROR_MIN and code <= ERROR_MAX:
                    self.handle_error(code, message)
            except:
                # non-numeric
                if words[1] == "PRIVMSG":
                    sender = words[0].lstrip(":")
                    receiver = words[2]
                    self.handle_privmsg(sender, receiver, message)
        else:
            self.handle_misc_message(words)

    def handle_numeric_reply(self, code, message):
        if code == RPL_MYINFO: # we're now actually connected
            self.join_all_channels()

    def handle_error(self, code, message):
        pass

    def handle_misc_message(self, words):
        if words[0] == "PING":
            if len(words) == 3:
                recipient = words[2]
            elif len(words) == 2:
                recipient = words[1].lstrip(":")
            else:
                return
            self.write("PONG %s" % recipient)
        elif words[0] == "ERROR":
            self.finish()

    def handle_privmsg(self, sender, receiver, message):
        name_parts = sender.split("!")
        sender_name = name_parts[0]
        sender_ident = name_parts[1]
        actions.action(self, sender_name, sender_ident, receiver, message)

    def send_private_message(self, receiver, message):
        prefix = "PRIVMSG %s :" % receiver
        msg_max = MAX_MSG - len(prefix)
        lines = list()
        while message != "":
            lines.append(message[0:msg_max])
            message = message[msg_max:]
        for line in lines:
            self.write(prefix + line)

    def quit(self, msg=""):
        self.write("QUIT :%s" % msg)
        # According to RFC we could just wait for ERROR message
        # but some networks (Quakenet, i look at thee) are just fucked up
        self.finish()

    def finish(self):
        self.done = True
        if self.ssl:
            del self.ssl
        self.socket.close()

def process_connections(connections):
    if len(connections) == 0:
        raise error, "Empty set of connections given"

    incoming, _, _ = select.select(connections, [], [])

    for c in incoming:
        c.process()
