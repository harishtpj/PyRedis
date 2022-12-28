import socket


def main():
    rserver = socket.create_server(("localhost", 6379), reuse_port=True)
    rserver.listen(5)

    while True:
        clnt, c_addr = rserver.accept()
        clnt.send(b"+PONG\r\n")


if __name__ == "__main__":
    main()
