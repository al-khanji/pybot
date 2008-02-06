import socket
import select
import actions

BUFSIZE = 4096
MAX_MSG = 450 # conservative
QUIT_MESSAGE = "My master bade me \"Quit thy lurking!\""

quit = False

class ConnectionError(Exception):
    pass

class Connection(object):
    def __init__(self, params):
        self.__dict__.update(params)
        self.left_over = ""

    def fileno(self):
        return self.socket.fileno()

    def write(self, message):
        print "<<<", message
        if not self.ssl:
            self.socket.sendall("%s\r\n" % message)
        else:
            self.ssl.write("%s\r\n" % message)

    def connect(self):
        self.socket = None
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
        self.write("NICK %s" % self.nick)
        self.write("USER %s %s dummy :%s" %
                          (self.nick, self.mode, self.realname))

    def join_channels(self):
        for chan in self.channels:
            self.write("JOIN %s" % chan)

    def process(self):
        if not self.ssl:
            data = self.left_over + self.socket.recv(BUFSIZE)
        else:
            data = self.left_over + self.ssl.read()
        self.left_over = ""

        lines = data.split("\r\n")
        if data[-2:] != "\r\n":
            self.left_over = lines.pop(-1)

        for line in lines:
            self.parse_line(line)

    def parse_line(self, line):
        if len(line.strip()) is 0:
            return

        print ">>>", repr(line)

        words = line.split()
        if line.startswith(":"):
            try:
                # numeric
                code = int(words[1])
            except:
                # non-numeric
                if words[1] == "PRIVMSG":
                    sender = words[0].lstrip(":")
                    receiver = words[2]
                    message = " ".join(words[3:]).lstrip(":")
                    self.parse_private_message(sender, receiver, message)
        else:
            if words[0] == "PING":
                self.write("PONG %s" % words[1])
            elif words[0] == "ERROR":
                global quit
                quit = "Yes please"

    def parse_private_message(self, sender, receiver, message):
        name_parts = sender.split("!")
        sender_name = name_parts[0]
        sender_ident = name_parts[1]

        if sender_name == "slougi" and message == "%s: quit" % self.nick:
            global quit
            quit = QUIT_MESSAGE

        if actions.match(message):
            response = actions.action(message)
            if receiver == self.nick:
                self.send_private_message(sender, response)
            else:
                self.send_private_message(receiver, response)

    def send_private_message(self, receiver, message):
        prefix = "PRIVMSG %s :" % receiver
        msg_max = MAX_MSG - len(prefix)
        lines = list()
        while message != "":
            lines.append(message[0:msg_max])
            message = message[msg_max:]
        for line in lines:
            self.write(prefix + line)

    def quit(self, msg):
        self.write("QUIT :%s" % msg)
        if self.ssl:
            del self.ssl
        self.socket.close()
        

def do_connections(connections):
    if len(connections) is 0:
        raise Exception, "Empty set of connections..."

    incoming, _, _ = select.select(connections, [], [])

    for c in incoming:
        c.process()
