import socket


def main():
    rserver = socket.create_server(("localhost", 6379), reuse_port=True)
    clnt, c_addr = rserver.accept()

    while True:
        data = clnt.recv(1024)
        clnt.send(b"+PONG\r\n")


if __name__ == "__main__":
    main()
