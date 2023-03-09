import socket
import pickle
from time import sleep

# -----Magic Numbers------#
proxy_sport = 8080
proxy_ip = '127.0.0.1'
proxy_address = (proxy_ip, proxy_sport)
# ------------------------#

def first_connection_with_proxy():
    #----opening socket----#
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(proxy_address)
    #----------------------#

    #----sending http request to get the site----#
    data = input("to get the site just write something \n")
    http_request = b"GET /index.html HTTP/1.1\r\nHost: site.html\r\n\r\n"
    client_socket.send(http_request)
    print("the client sent the http request for the site\n")
    #--------------------------------------------#


    #----receiving the site----#
    the_site = client_socket.recv(8192)
    print("the client received the http response for the site\n")
    the_site = the_site.decode("utf-8")
    temp = the_site.find("<")
    the_site = the_site[temp:]
    fp = open("TheSite.html", "a+")
    fp.write(the_site)
    fp.close()
    print("The Client has the site and now he can open it\n")
    #--------------------------#

    #----closing socket----#
    client_socket.close()
    print("finished the first connection + closed sockets\n")
    #----------------------#




def ask_image_1(sock):
    #----send http request to get an object from the site----#
    print("\n")
    http_request = b"GET /index.jpg HTTP/1.1\r\nHost: image1.jpg\r\n\r\n"
    sock.send(http_request)
    print("the client sent the http request for the object")
    #--------------------------------------------------------#

    #----receive the size of the object----#
    size_of_image = sock.recv(8192)
    size_of_image = int.from_bytes(size_of_image, 'big')
    print("the client received the size of the image: " + str(size_of_image))
    #--------------------------------------#

    #----receive the object----#
    current_size = 0
    fp = open("first_image.jpg", "ab")
    while current_size < size_of_image:
        temp = sock.recv(8192)
        fp.write(temp)
        current_size = current_size + len(temp)
    fp.close()
    http_response = sock.recv(8192).decode("utf-8")
    print("the client received the image number 1. \n")
    #--------------------------#



def ask_image_2(sock):
    print("\n")
    http_request = b"GET /index.jpg HTTP/1.1\r\nHost: image2.jpeg\r\n\r\n"
    sock.send(http_request)
    print("the client sent the http request for the object")
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
    print("the client received the image number 2. \n")



def ask_image_3(sock):
    print("\n")
    http_request = b"GET /index.jpg HTTP/1.1\r\nHost: image3.jpeg\r\n\r\n"
    sock.send(http_request)
    print("the client sent the http request for the object")
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
    print("the client received the image number 3. \n")




if __name__ == "__main__":
    print("hello I am the client")
    first_connection_with_proxy()

    #----loop for requesting objects----#
    while True:
        client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket1.connect(proxy_address)
        data = input("press 1 to get the first image, 2 to get the second image, 3 to get the third image: \n")
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
            break



