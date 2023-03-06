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
    loop_num = 0
    while True:
        loop_num = loop_num + 1

        # receiving data from user
        data = input("pls enter a site you want to get: ")
        print("\n")

        # option for closing the socket
        if data == "stop":
            data = data.encode()
            client.sendto(data, (proxy_ip, proxy_sport))
            print("---The client has successfully disconnected from the server")
            break

        # sending a requested site to the proxy
        request(data)

        # we want to get ack from the proxy
        data, addr = client.recvfrom(1024)

        # get ack for sending request
        check_ack(data, "for getting the site")

        # we want to get the site from the proxy
        html_file, addr = client.recvfrom(1024)
        fp = open("TheSite.html", "a")
        html_file = html_file.decode("utf-8")

        start_index = html_file.find("<", 0, len(html_file))
        html_file = html_file[start_index:len(html_file)]

        fp.write(html_file)
        fp.close()
        print("got the site from the proxy - example.com\n")

        # send ack
        send_ack("for getting the site")

        # here we want to choose what file we want
        file_name = input("What file do you want")
        file_num = file_name[len(file_name) - 1:len(file_name)]
        print(file_num)
        print("requesting " + file_name)
        file_name = file_name.encode()
        sleep(1)
        client.sendto(file_name, (proxy_ip, proxy_sport))

        # receiving ack from proxy
        data, addr = client.recvfrom(1024)
        check_ack(data, "for requesting the file")



        file_txt = open("file_" + file_num + ".txt", "a+")
        file_size, addr = client.recvfrom(1024)
        file_size = int.from_bytes(file_size, "big")
        # client.settimeout(3)
        packet_sequence = [0]
        current_ack = 1
        window_size = 1
        tmp = 0
        Flag = 1
        current_file_size = 0
        while file_size > current_file_size:
            while int(window_size) > tmp:
                tmp += 1
                # try:
                file, addr = client.recvfrom(1024)
                file = file.decode("utf-8")
                file = file.split("&")
                window_size = file[0]
                print(window_size)
                file[1] = file[1].split("$")
                if (not packet_sequence.__contains__(int(file[1][0]))) and current_ack == int(file[1][0]):
                    current_ack += 1
                    packet_sequence.append(int(file[1][0]))
                    file_txt.write(file[1][1])
                    current_file_size += len(file[1][1])
                # except:
                #     print("timeout")


            tmp = 0
            while Flag < current_ack:
                sleep(1)
                data = "packet " + str(Flag)
                data = data.encode()
                client.sendto(data, (proxy_ip, proxy_sport))
                print("sent ack for " + data.decode("utf-8"))
                Flag += 1

            print("the size is: " + str(current_file_size))

        file_txt.close()

    # close the socket
    client.close()
    print("---Successfully closed the socket")