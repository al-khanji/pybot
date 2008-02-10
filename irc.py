# Copyright (c) 2008 Louai Al-Khanji

import socket
import select
import logging
import actions

BUFSIZE = 4096
MAX_MSG = 420 # conservative
LINE_BREAK = "\r\n"

quit = False

class ConnectionError(Exception):
    pass

class Connection(object):
    def __init__(self, params):
        self.__dict__.update(params)
        self._leftover = ""

    def fileno(self):
        return self.socket.fileno()

    def write(self, message):
        logging.info("<<<", repr(message))
        if self.ssl:
            self.ssl.write("%s%s" % (message, LINE_BREAK))
        else:
            self.socket.sendall("%s%s" % (message, LINE_BREAK))

    def connect(self):
        self.socket = None
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

    def join_channels(self):
        for chan in self.channels:
            self.write("JOIN %s" % chan)

    def process(self):
        if self.ssl:
            data = self._leftover + self.ssl.read()
        else:
            data = self._leftover + self.socket.recv(BUFSIZE)

        lines = data.split(LINE_BREAK)
        if data[-2:] != LINE_BREAK:
            self._leftover = lines.pop(-1)
        else:
            self._leftover = ""

        for line in lines:
            self.parse_line(line)

    def parse_line(self, line):
        line = line.strip()
        if len(line) is 0:
            return

        logging.info(">>>", repr(line))

        words = line.split()
        if line.startswith(":"):
            try:
                # numeric
                code = int(words[1])
                message = " ".join(words[3:]).lstrip(":")
                if code >= 1 and code <= 399:
                    self.handle_numeric_reply(code, message)
                elif code >= 400 and code <= 599:
                    self.handle_error(code, message)
            except:
                # non-numeric
                if words[1] == "PRIVMSG":
                    sender = words[0].lstrip(":")
                    receiver = words[2]
                    message = " ".join(words[3:]).lstrip(":")
                    self.handle_privmsg(sender, receiver, message)
        else:
            if words[0] == "PING":
                self.write("PONG %s" % words[1])
            elif words[0] == "ERROR":
                global quit
                quit = True
                if self.ssl:
                    del self.ssl
                self.socket.close()

    def handle_numeric_reply(self, code, message):
        if code == 4: # we're now actually connected
            self.join_channels()

    def handle_error(self, code, message):
        pass

    def handle_privmsg(self, sender, receiver, message):
        name_parts = sender.split("!")
        sender_name = name_parts[0]
        sender_ident = name_parts[1]

        if sender_name == "slougi" and message == "%s: quit" % self.nick:
            global quit
            quit = True

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

    def quit(self):
        self.write("QUIT :%s" % self.quit_message)

def do_connections(connections):
    if len(connections) is 0:
        raise Exception, "Empty set of connections..."

    incoming, _, _ = select.select(connections, [], [])

    for c in incoming:
        c.process()
