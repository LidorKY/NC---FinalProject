import socket
from time import sleep

server_files_sport = 80

server_files = '127.0.0.1'


def file_1(ans_socket):
    print("in file 1")
    fp = open("1.txt", "r")

    txt = fp.read()

    fp.close()

    size = str(len(txt))

    ans_socket.send(size.encode())

    http_response = "HTTP/1.1 200 OK\r\nContent_Type: text/txt\r\n\r\n" + txt

    http_response = http_response.encode()

    sleep(1)

    ans_socket.sendall(http_response)

    print("sent file_1\n")


def file_2(ans_scoket):
    print("in file 2")
    fp = open("2.txt", "r")

    txt = fp.read()

    fp.close()

    size = str(len(txt))

    ans_socket.send(size.encode())

    http_response = "HTTP/1.1 200 OK\r\nContent_Type: text/txt\r\n\r\n" + txt

    http_response = http_response.encode()

    sleep(1)

    ans_socket.sendall(http_response)

    print("sent file_2\n")


def file_3(ans_socket):
    print("in file 3")
    fp = open("3.txt", "r")

    txt = fp.read()

    fp.close()

    size = str(len(txt))

    ans_socket.send(size.encode())

    http_response = "HTTP/1.1 200 OK\r\nContent_Type: text/txt\r\n\r\n" + txt

    http_response = http_response.encode()

    sleep(1)

    ans_socket.sendall(http_response)

    print("sent file_3\n")


if __name__ == "__main__":

    print("Hello I am the server that has the files\n")

    server_site_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_site_tcp.bind((server_files, 30714))

    server_site_tcp.listen(1)
    print("listening...\n")
    while True:
        ans_socket, ans_addr = server_site_tcp.accept()
        request = ans_socket.recv(1024).decode()
        print("got http request\n")
        if request == "stop":
            print("goodbye")
            break

        start_index = request.find("f", 0, len(request))
        request = request[start_index:len(request)]

        if request == "file_1":
            file_1(ans_socket)
        elif request == "file_2":
            file_2(ans_socket)
        elif request == "file_3":
            file_3(ans_socket)
        else:
            print("error")
            break

    ans_socket.close()
    print("closed socket...\n")
    print("finished!!!")