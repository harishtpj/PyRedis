# Module to decode RESP Strings

class ConnectionBuffer:
    def __init__(self, connection):
        self.connection = connection
        self.buffer = b''

    def read_until_delimiter(self, delimiter):
        while delimiter not in self.buffer:
            data = self.connection.recv(1024)

            if not data:
                return None

            self.buffer += data

        data_before_delimiter, delimiter, self.buffer = self.buffer.partition(delimiter)
        return data_before_delimiter

    def read(self, bufsize):
        if len(self.buffer) < bufsize:
            data = self.connection.recv(1024)

            if not data:
                return None

            self.buffer += data

        data, self.buffer = self.buffer[:bufsize], self.buffer[bufsize:]
        return data

class RESPDecoder:
    def __init__(self, conn):
        self.conn = ConnectionBuffer(conn)

    def decode(self):
        dt_byte = self.conn.read(1)

        if dt_byte == b'+':
            return self.decode_simple_str()
        elif dt_byte == b'$':
            return self.decode_bulk_str()
        elif dt_byte == b'*':
            return self.decode_array()
        else:
            raise Exception(f"Unknown data type byte: {dt_byte}")
    
    def decode_simple_str(self):
        return self.conn.read_until_delimiter(b"\r\n")
    
    def decode_bulk_str(self):
        bulk_string_len = int(self.conn.read_until_delimiter(b"\r\n"))
        data = self.conn.read(bulk_string_len)
        assert data is not None, "Connection closed before bulk string could be read"
        assert self.conn.read_until_delimiter(b"\r\n") == b""
        return data
    
    def decode_array(self):
        result = []
        arr_len = int(self.conn.read_until_delimiter(b"\r\n"))

        for _ in range(arr_len):
            result.append(self.decode())

        return result
