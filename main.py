import socket


HOST = '0.0.0.0'
PORT = 50007

# 소켓 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print('binding')
    s.bind((HOST, PORT))
    print('listening')
    s.listen(1)

    conn, addr = s.accept()

    with conn:
        print('connected {}:{}'.format(addr[0], addr[1]))
        while True:
            data = conn.recv(1024)
            print('data: {}'.format(str(data)))
            if not data:
                break
            conn.send(b'hey')