import os
import socket
import stat
import sys
from webbrowser import open_new_tab

#-----Magic Numbers------#
proxy_sport = 20230
proxy_ip = '127.0.0.1'
#------------------------#



def check(data):
    if data == "stop":
        data = data.encode()
        client.sendto(data, (proxy_ip, proxy_sport))
        client.close()
        print("---The client has successfully disconected from the server")
        return



def request(data):
    data = data.encode()
    client.sendto(data, (proxy_ip, proxy_sport))
    print("sent request to proxy")



def check_ack(data):
    if data.decode("utf-8") != 'ack':
        print("error")
        return
    else:
        print("got ack - for requesting the site")



def send_ack():
    data = 'ack'
    data = data.encode()
    client.sendto(data, (proxy_ip, proxy_sport))
    print("sent ack for getting the site\n")



if __name__ == "__main__":

    # using UDP protocol
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # the loop for receiving and sending the data
    print("hello I am the client\n")
    while True:

        # receiving data from user
        data = input("pls enter a site you want to get: ")
        print("\n")

        #option for closing the socket
        check(data)


        #sending a requested site to the proxy
        request(data)


        #we want to get ack from the proxy
        data, addr = client.recvfrom(1024)


        #get ack for sending request
        check_ack(data)


        # we want to get the site from the proxy
        html_file, addr = client.recvfrom(1024)
        fp = open("TheSite.html", "a")
        html_file = html_file.decode("utf-8")

        start_index = html_file.find("<", 0, len(html_file))
        html_file = html_file[start_index:len(html_file)]

        fp.write(html_file)
        fp.close()
        print("get the site from the proxy - example.com\n")


        # send ack
        send_ack()




    # close the socket
    client.close()
    print("---Successfully closed the socket")


