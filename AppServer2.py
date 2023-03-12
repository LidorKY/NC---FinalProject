import socket
from time import sleep

# ------Magic Numbers-------#
server_objects_sport = 7104
server_objects_ip = '127.0.0.1'
server_objects_address = (server_objects_ip, server_objects_sport)
# --------------------------#



def image_1(ans_socket):
    #----send http response----#
    print("sending image number 1")
    http_response = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\nimage1.jpeg"
    ans_socket.send(http_response)
    #--------------------------#



def image_2(ans_socket):
    print("sending image number 2")
    http_response = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\n\r\nimage2.jpg"
    ans_socket.send(http_response)



def image_3(ans_socket):
    print("sending image number 3")
    http_response = b"HTTP/1.1 200 OK\r\nContent-Type: image/jpg\r\n\r\nimage3.jpg"
    ans_socket.send(http_response)



if __name__ == "__main__":

    print("Hello I am the server that has the files\n")
    server_site_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_site_tcp.bind(server_objects_address)
    server_site_tcp.listen(1)
    print("listening...\n")
    while True:
        ans_socket, ans_addr = server_site_tcp.accept()
        request = ans_socket.recv(8192).decode("utf-8")
        print("got http request: \n")

        if "image1.jpg" in request:
            image_1(ans_socket)
        elif "image2.jpg" in request:
            image_2(ans_socket)
        elif "image3.jpg" in request:
            image_3(ans_socket)
        else:
            print("error")
            break


        ans_socket.close()
        print("closed socket...\n")

    ans_socket.close()
    print("closed socket...\n")