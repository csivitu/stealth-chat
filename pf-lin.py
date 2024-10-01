import socket
import threading
import logging
from string import ascii_lowercase as lc, ascii_uppercase as uc

def rot_enc(n):
    lookup = str.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
    return lambda s: s.translate(lookup)

def rot_dec(n):
    return rot_enc(-n)

format = '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=format)

def handle(buffer, direction, src_address, src_port, dst_address, dst_port) -> bytes:
    if direction:
        bydata = rot_enc(key)(buffer.decode()).encode()
        logging.debug(f"{src_address, src_port} -> {dst_address, dst_port} {len(buffer)} bytes")
    else:
        bydata = rot_dec(key)(buffer.decode()).encode()
        logging.debug(f"{src_address, src_port} <- {dst_address, dst_port} {len(bydata)} bytes")
    return bydata

def transfer(src, dst, direction):
    src_address, src_port = src.getsockname()
    dst_address, dst_port = dst.getsockname()
    while True:
        try:
            buffer = src.recv(1024)
            if len(buffer) == 0:
                break
            dst.send(handle(buffer, direction, src_address, src_port, dst_address, dst_port))
        except Exception as e:
            logging.error(repr(e))
            break
    logging.warning(f"Closing connect {src_address, src_port}! ")
    src.close()
    logging.warning(f"Closing connect {dst_address, dst_port}! ")
    dst.close()

def server(local_host, local_port, remote_host, remote_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(0x40)
    logging.info(f"Server started {local_host, local_port}")
    logging.info(f"Connect to {local_host, local_port} to get the content of {remote_host, remote_port}")
    while True:
        src_socket, src_address = server_socket.accept()
        logging.info(f"[Establishing] {src_address} -> {local_host, local_port} -> ? -> {remote_host, remote_port}")
        try:
            dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dst_socket.connect((remote_host, remote_port))
            logging.info(f"[OK] {src_address} -> {local_host, local_port} -> {dst_socket.getsockname()} -> {remote_host, remote_port}")
            s = threading.Thread(target=transfer, args=(dst_socket, src_socket, False))
            r = threading.Thread(target=transfer, args=(src_socket, dst_socket, True))
            s.start()
            r.start()
        except Exception as e:
            logging.error(repr(e))

def main():
    # server(listen_host, listen_port, connect_host, connect_port)
    server("127.0.0.1", 5555, "127.0.0.1", 7777)

if __name__ == "__main__":
    passw = input("Enter pass: ")
    key = sum(map(ord, passw))
    main()