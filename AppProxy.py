from socket import *
from scapy.all import *


#------Magic Numbers-------#
proxy_sport = 20230
proxy_ip = '127.0.0.1'
server_site_sport = 80
server_site = '127.0.0.1'
server_files_sport = 80
server_files = '127.0.0.1'
#--------------------------#




def Connection_with_server_site():
    print("connecting to site server")
    proxy_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_site_address = (server_site, server_site_sport)

    proxy_tcp.connect(server_site_address)

    http_request = b"GET /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n"

    proxy_tcp.sendall(http_request)
    print("sent http request")

    http_response = proxy_tcp.recv(1024)
    http_response = http_response.decode("utf-8")
    print("got http response")

    proxy_tcp.close()
    print("closed tcp socket")
    return http_response



def get_ack(data1):
    if data1.decode("utf-8") != 'ack':
        print("error")
        return

    else:
        print("got ack - for receiving the html file")



def send_ack(address1):
    # ack
    data = 'ack'

    # encoding the data
    data = data.encode()

    # send the ack back to the client
    porxy_udp.sendto(data, address1)
    print("sent ack to client")



def ask_file_1():
    print("asking for file_1")
    print("connecting to files server")
    proxy_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_files_address = (server_files, 30714)  # need to change the port

    proxy_tcp.connect(server_files_address)

    http_request = b"GET /index.html HTTP/1.1\r\nHost: file_1"

    proxy_tcp.sendall(http_request)
    print("sent http request for file_2")

    # getting the size of file_2
    num = proxy_tcp.recv(1024)
    num = num.decode("utf-8")
    num = int(num)
    temp = ''
    file = ''

    while num != len(file):
        temp = proxy_tcp.recv(1024)
        temp = temp.decode("utf-8")
        temp = temp[len(temp) - num:len(temp)]
        print(temp)
        file += temp
        print(len(file))

    proxy_tcp.close()
    print("closed tcp socket")
    return file




def ask_file_2():
    print("asking for file_2")
    print("connecting to files server")
    proxy_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_files_address = (server_files, 30714)

    proxy_tcp.connect(server_files_address)

    http_request = b"GET /index.html HTTP/1.1\r\nHost: file_2"

    proxy_tcp.sendall(http_request)
    print("sent http request for file_2")

    #getting the size of file_2
    num = proxy_tcp.recv(1024)
    num = num.decode("utf-8")
    num = int(num)
    temp = ''
    file = ''

    while num != len(file):
        temp = proxy_tcp.recv(1024)
        temp = temp.decode("utf-8")
        temp = temp[len(temp)-num:len(temp)]
        print(temp)
        file += temp
        print(len(file))


    proxy_tcp.close()
    print("closed tcp socket")
    return file


def ask_file_3():
    print("asking for file_3")
    print("connecting to files server")
    proxy_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_files_address = (server_files, 30714) # need to change the port

    proxy_tcp.connect(server_files_address)

    http_request = b"GET /index.html HTTP/1.1\r\nHost: file_3"

    proxy_tcp.sendall(http_request)
    print("sent http request for file_2")

    # getting the size of file_2
    num = proxy_tcp.recv(1024)
    num = num.decode("utf-8")
    num = int(num)
    temp = ''
    file = ''

    while num != len(file):
        temp = proxy_tcp.recv(1024)
        temp = temp.decode("utf-8")
        temp = temp[len(temp) - num:len(temp)]
        print(temp)
        file += temp
        print(len(file))

    proxy_tcp.close()
    print("closed tcp socket")
    return file




if __name__ == "__main__":

    # using UDP protocol
    porxy_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # local host and port
    porxy_udp.bind((proxy_ip, proxy_sport))

    # the loop for receiving and sending the data
    print("hello I am the Proxy server - the actual app\n")
    while True:
        # receiving data
        data, address = porxy_udp.recvfrom(1024)
        print("got message from client")

        # decoding tha data
        data = data.decode("utf-8")

        if data == "stop":
            print("Client has been successfully disconnected")
            break

        # print for check
        print("The data: ", data)

        send_ack(address)



########################################################################################################################

        #want to go to server that holds the site - now tcp connection

        resp = Connection_with_server_site()

######################################################################################################################

        # send the site to the client
        print("responding to client")
        resp = resp.encode()
        porxy_udp.sendto(resp, address)


        # receiving ack
        data, address = porxy_udp.recvfrom(1024)

        get_ack(data)




#---------------------#

        # receiving which file the client wants
        data, address = porxy_udp.recvfrom(1024)

        data = data.decode("utf-8")

        #need to send ack for getting request for a file



        if data == "file_1":
            file_1 = ask_file_1()
        if data == "file_2":
            file_2 = ask_file_2()
        if data == "file_3":
            file_3 = ask_file_3()
        else:
            print("error")


        #need to send it to the client and get ack for it

# ---------------------#

        print("finish!!!")
        break





    #close the socket
    porxy_udp.close()
    print("---Successfully closed the socket")
