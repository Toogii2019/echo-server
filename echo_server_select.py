import socket
import sys
import traceback
import select


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    # TODO: Replace the following line with your code which will instantiate
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # TODO: You may find that if you repeatedly run the server script it fails,
    #       claiming that the port is already used.  You can set an option on
    #       your socket that will fix this problem. We DID NOT talk about this
    #       in class. Find the correct option by reading the very end of the
    #       socket library documentation:
    #       http://docs.python.org/3/library/socket.html#example

    # =========== SELECT ============= #
    inputs = [sock]
    outputs = []
    # ================================ #
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # TODO: bind your new sock 'sock' to the address above and begin to listen
    #       for incoming connections
    sock.bind(address)
    sock.listen()
    msg_recvd = b''
    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # =========== SELECT ============= #
            while inputs:
                read, write, error = select.select(inputs, outputs, inputs)
                for s in read:
                    if s is sock:
                        conn, addr = s.accept()
                        print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                        inputs.append(conn)
                    else:
                        data = s.recv(1024)
                        if data:
                            print('received "{0}"'.format(data.decode('utf8')))
                            msg_recvd = data
                            if s not in outputs:
                                outputs.append(s)
                        else:
                            if s in outputs:
                                outputs.remove(s)
                                s.close()

                for s in write:
                    if msg_recvd:
                        s.send(msg_recvd)
                        print('sent "{0}"'.format(msg_recvd.decode('utf8')))
                        msg_recvd = b''
                    else:
                        outputs.remove(s)
                for s in error:
                    inputs.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                        s.close()

            # ================================ #
    except KeyboardInterrupt:
        # TODO: Use the python KeyboardInterrupt exception as a signal to
        #       close the server socket and exit from the server function.
        #       Replace the call to `pass` below, which is only there to
        #       prevent syntax problems
        conn.close()
        print('quitting echo server', file=log_buffer)
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
