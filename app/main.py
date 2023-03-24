import socket
import threading

def handle_conn(clnt):
    while True:
        try:
            clnt.recv(1024)
            clnt.send(b"+PONG\r\n")
        except ConnectionError:
            break

def main():
    rserver = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        clnt, c_addr = rserver.accept()
        threading.Thread(target=handle_conn, args=(clnt,)).start()


if __name__ == "__main__":
    main()
