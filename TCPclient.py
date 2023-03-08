import socket
import pickle
from time import sleep

# -----Magic Numbers------#
proxy_sport = 8080
proxy_ip = '127.0.0.1'
proxy_address = (proxy_ip, proxy_sport)
# ------------------------#


if __name__ == "__main__":
    print("hello I am the client")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(proxy_address)
    data = input("pls enter a name of site: \n")

    http_request = b"GET /index.html HTTP/1.1\r\nHost: site.html\r\n\r\n"
    client_socket.send(http_request)
    print("the client sent the http request for the site")

    the_site = client_socket.recv(8192)
    print("the client received the http response for the site")

    the_site = the_site.decode("utf-8")
    temp = the_site.find("<")
    the_site = the_site[temp:]

    fp = open("TheSite.html", "a+")
    fp.write(the_site)
    fp.close()

    print("The Client has the site and now he can open it")

    client_socket.close()
    print("finished + closed sockets")

    #opening socket another time to get images
































