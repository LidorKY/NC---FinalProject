import socket
import pickle
from time import sleep

# -----Magic Numbers------#
proxy_sport = 8080
proxy_ip = '127.0.0.1'
proxy_address = (proxy_ip, proxy_sport)
# ------------------------#

def first_connection_with_proxy():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(proxy_address)
    data = input("pls enter a name of site: \n")

    http_request = b"GET /index.html HTTP/1.1\r\nHost: site.html\r\n\r\n"
    client_socket.send(http_request)
    print("the client sent the http request for the site\n")

    the_site = client_socket.recv(8192)
    print("the client received the http response for the site\n")

    the_site = the_site.decode("utf-8")
    temp = the_site.find("<")
    the_site = the_site[temp:]

    fp = open("TheSite.html", "a+")
    fp.write(the_site)
    fp.close()

    print("The Client has the site and now he can open it\n")

    client_socket.close()
    print("finished the first connection + closed sockets\n")




def ask_image_1(sock):
    print("\n")
    http_request = b"GET /index.jpg HTTP/1.1\r\nHost: image1.jpg\r\n\r\n"
    sock.send(http_request)
    print("the client sent the http request for the site")

    size_of_image = sock.recv(8192)
    size_of_image = int.from_bytes(size_of_image, 'big')
    print("the client received the size of the image: " + str(size_of_image))

    current_size = 0
    fp = open("first_image.jpg", "ab")

    while current_size < size_of_image:
        temp = sock.recv(8192)
        fp.write(temp)
        current_size = current_size + len(temp)
    fp.close()

    http_response = sock.recv(8192).decode("utf-8")


def ask_image_2(sock):
    print("\n")
    http_request = b"GET /index.jpg HTTP/1.1\r\nHost: image2.jpeg\r\n\r\n"
    sock.send(http_request)
    print("the client sent the http request for the site")

    size_of_image = sock.recv(8192)
    size_of_image = int.from_bytes(size_of_image, 'big')
    print("the client received the size of the image: " + str(size_of_image))

    current_size = 0
    fp = open("second_image.jpeg", "ab")

    while current_size < size_of_image:
        temp = sock.recv(8192)
        fp.write(temp)
        current_size = current_size + len(temp)
    fp.close()

    http_response = sock.recv(8192).decode("utf-8")


def ask_image_3(sock):
    print("\n")
    http_request = b"GET /index.jpg HTTP/1.1\r\nHost: image3.jpeg\r\n\r\n"
    sock.send(http_request)
    print("the client sent the http request for the site")

    size_of_image = sock.recv(8192)
    size_of_image = int.from_bytes(size_of_image, 'big')
    print("the client received the size of the image: " + str(size_of_image))

    current_size = 0
    fp = open("third_image.jpeg", "ab")

    while current_size < size_of_image:
        temp = sock.recv(8192)
        fp.write(temp)
        current_size = current_size + len(temp)
    fp.close()

    http_response = sock.recv(8192).decode("utf-8")



if __name__ == "__main__":
    print("hello I am the client")
    first_connection_with_proxy()
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(proxy_address)
    # data = input("pls enter a name of site: \n")
    #
    # http_request = b"GET /index.html HTTP/1.1\r\nHost: site.html\r\n\r\n"
    # client_socket.send(http_request)
    # print("the client sent the http request for the site")
    #
    # the_site = client_socket.recv(8192)
    # print("the client received the http response for the site")
    #
    # the_site = the_site.decode("utf-8")
    # temp = the_site.find("<")
    # the_site = the_site[temp:]
    #
    # fp = open("TheSite.html", "a+")
    # fp.write(the_site)
    # fp.close()
    #
    # print("The Client has the site and now he can open it")
    #
    # client_socket.close()
    # print("finished + closed sockets")

    while True:
        #opening socket another to get images
        client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket1.connect(proxy_address)
        data = input("press 1 to get the first image, 2 to get the second image, 3 to get the third image")

        if data == "1":
            print("first image on her way")
            ask_image_1(client_socket1)
        elif data == "2":
            print("second image on her way")
            ask_image_2(client_socket1)
        elif data == "3":
            print("third image on her way")
            ask_image_3(client_socket1)
        else:
            print("error")
            client_socket1.close()
            print("closed the client's socket")

        #
        # http_request = b"GET /index.jpg HTTP/1.1\r\nHost: image1.jpg\r\n\r\n"
        # client_socket1.send(http_request)
        # print("the client sent the http request for the site")
        #
        # size_of_image = client_socket1.recv(8192)
        # size_of_image = int.from_bytes(size_of_image, 'big')
        # print("the client received the size of the image: " + str(size_of_image))
        #
        # current_size = 0
        # fp = open("first_image.jpg", "ab")
        #
        # while current_size < size_of_image:
        #     temp = client_socket1.recv(8192)
        #     fp.write(temp)
        #     current_size = current_size + len(temp)
        #
        # fp.close()
        #
        # print("got first object")
        # client_socket1.close()
        # print("closed the clients socket")




































