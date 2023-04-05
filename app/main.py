from .resp import RESPDecoder
import socket, threading

class RedisDB(dict):
    def set(self, key, val):
        self.__dict__[key] = val
    
    def get(self, key):
        return self.__dict__[key]
    

def handle_conn(clnt, db):
    while True:
        try:
            cmd, *args = RESPDecoder(clnt).decode()
            
            response = b"-ERR unknown command\r\n"
            if cmd == b"ping":
                response = b"+PONG\r\n"
            elif cmd == b"echo":
                response = b"$%d\r\n%b\r\n" % (len(args[0]), args[0])
            elif cmd == b"set":
                db.set(args[0], args[1])
                response = b"+OK\r\n"
            elif cmd == b"get":
                val = db.get(args[0])
                response = b"%d\r\n%b\r\n" % (len(val), val) if val else "$-1\r\n"

            clnt.send(response)
        except ConnectionError:
            break

def main():
    rdb = RedisDB()
    rserver = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        clnt, c_addr = rserver.accept()
        print(f"Connected to {c_addr}")
        threading.Thread(target=handle_conn, args=(clnt, rdb,)).start()


if __name__ == "__main__":
    main()
