import socket
import pickle
from time import sleep

# -----Magic Numbers------#
proxy_sport = 20230
proxy_ip = '127.0.0.1'
# ------------------------#

def request(data):
    data = data.encode()
    client.sendto(data, (proxy_ip, proxy_sport))
    print("sent request to proxy")


def check_ack(data, str):
    if data.decode("utf-8") != 'ack':
        print("error")
        return
    else:
        print("got ack - " + str)


def send_ack(str):
    data = 'ack'
    data = data.encode()
    client.sendto(data, (proxy_ip, proxy_sport))
    print("sent ack for " + str)


if __name__ == "__main__":

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # the loop for receiving and sending the data
    print("hello I am the client\n")
    # receiving data from user
    data = input("pls enter a site you want to get: ")
    print("\n")
    # sending a requested site to the proxy
    request(data)

    # we want to get ack from the proxy for the requested site
    data, addr = client.recvfrom(8192)
    # get ack for sending request
    check_ack(data, "for getting the site")


    #----receiving the site----#
    html_file, addr = client.recvfrom(8192)
    fp = open("TheSite.html", "a+")
    html_file = html_file.decode("utf-8")
    start_index = html_file.find("<")
    html_file = html_file[start_index:]
    fp.write(html_file)
    fp.close()
    print("got the site from the proxy - site.html\n")
    #--------------------------#

    # send ack
    send_ack("for getting the site")


    while True:
        # here we want to choose what object we want
        file_name = input("press 1 for the first object, 2 for the second object and 3 for the third object: \n")
        if file_name == "1":
            file_name = "image1.jpg"
            temp1 = "first_image.jpg"
        elif file_name == "2":
            file_name = "image2.jpg"
            temp1 = "second_image.jpg"
        elif file_name == "3":
            file_name = "image3.jpg"
            temp1 = "third_image.jpg"
        else:
            print("error")
        print("requesting " + str(file_name))
        file_name = file_name.encode()
        client.sendto(file_name, (proxy_ip, proxy_sport))


        # receiving ack from proxy
        data, addr = client.recvfrom(8192)
        check_ack(data, "for requesting object")

        #receiving the size of the object
        size_of_image, addr = client.recvfrom(8192)
        size_of_image = int.from_bytes(size_of_image, 'big')
        send_ack("receiving the objects size")
        print("the size of the object is: " + str(size_of_image))

        # ----receive the object----#
        current_size = 0
        fp = open(temp1, "ab")
        while current_size < size_of_image:
            data, addr = client.recvfrom(8192)
            fp.write(data)
            current_size = current_size + len(data)
            print(current_size)
        fp.close()
        send_ack("receiving the object")
        print("the client received the image number 1. \n")
        # --------------------------#












    # file_txt = open("file_" + file_num + ".txt", "a+")
    # file_size, addr = client.recvfrom(1024)
    # file_size = int.from_bytes(file_size, "big")
    # # client.settimeout(3)
    # packet_sequence = [0]
    # current_ack = 1
    # window_size = 1
    # tmp = 0
    # Flag = 1
    # current_file_size = 0
    # while file_size > current_file_size:
    #     while int(window_size) > tmp:
    #         tmp += 1
    #         # try:
    #         file, addr = client.recvfrom(1024)
    #         file = file.decode("utf-8")
    #         file = file.split("&")
    #         window_size = file[0]
    #         print(window_size)
    #         file[1] = file[1].split("$")
    #         if (not packet_sequence.__contains__(int(file[1][0]))) and current_ack == int(file[1][0]):
    #             current_ack += 1
    #             packet_sequence.append(int(file[1][0]))
    #             file_txt.write(file[1][1])
    #             current_file_size += len(file[1][1])
    #         # except:
    #         #     print("timeout")
    #
    #
    #     tmp = 0
    #     while Flag < current_ack:
    #         sleep(1)
    #         data = "packet " + str(Flag)
    #         data = data.encode()
    #         client.sendto(data, (proxy_ip, proxy_sport))
    #         print("sent ack for " + data.decode("utf-8"))
    #         Flag += 1
    #
    #     print("the size is: " + str(current_file_size))
    #
    # file_txt.close()

    # close the socket
    client.close()
    print("---Successfully closed the socket")