from .resp import RESPDecoder
import socket, threading

def handle_conn(clnt):
    while True:
        try:
            cmd, *args = RESPDecoder(clnt).decode()

            if cmd == b"ping":
                clnt.send(b"+PONG\r\n")
            elif cmd == b"echo":
                clnt.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))
            else:
                clnt.send(b"-ERR unknown command\r\n")
        except ConnectionError:
            break

def main():
    rserver = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        clnt, c_addr = rserver.accept()
        threading.Thread(target=handle_conn, args=(clnt,)).start()


if __name__ == "__main__":
    main()
