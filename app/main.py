from .resp import RESPDecoder
import socket, threading, time

class RedisDB(dict):
    def setval(self, key, val):
        self.__dict__[key] = val
    
    def get(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return None
    
    def delkey(self, key):
        del self.__dict__[key]

db = RedisDB()

def del_exp_key(key, ms):
    time.sleep(ms/1000)
    db.delkey(key)

def handle_conn(clnt):
    while True:
        try:
            cmd, *args = RESPDecoder(clnt).decode()
            print(f"Received command: {cmd}")
            
            response = b"-ERR unknown command\r\n"
            if cmd == b"ping":
                response = b"+PONG\r\n"
            elif cmd == b"echo":
                response = b"$%d\r\n%b\r\n" % (len(args[0]), args[0])
            elif cmd == b"set":
                if len(args) < 2:
                    response = b"-ERR wrong number of arguments for 'set' command\r\n"
                else:
                    db.setval(args[0], args[1])
                    print(f"Inserted key {args[0]} with val {db.get(args[0])}")
                    if len(args) == 4:
                        if args[2] == b"px":
                            threading.Thread(target=del_exp_key, args=(args[0], int(args[3]),)).start()
                    response = b"+OK\r\n"
            elif cmd == b"get":
                if len(args) != 1:
                    response = b"-ERR wrong number of arguments for 'get' command\r\n"
                else:
                    val = db.get(args[0])
                    response = b"$%d\r\n%b\r\n" % (len(val), val) if val else b"$-1\r\n"

            clnt.send(response)
        except ConnectionError:
            break

def main():
    rserver = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        clnt, c_addr = rserver.accept()
        print(f"Connected to {c_addr}")
        threading.Thread(target=handle_conn, args=(clnt,)).start()

if __name__ == "__main__":
    main()
