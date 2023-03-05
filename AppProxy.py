import pickle
from socket import *
from scapy.all import *
import numpy

# ------Magic Numbers-------#
proxy_sport = 20230
proxy_ip = '127.0.0.1'
server_site_sport = 80
server_site = '127.0.0.1'
server_files_sport = 80
server_files = '127.0.0.1'


# --------------------------#


def Connection_with_server_site(proxy_tcp_server):
    http_request = b"GET /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n"
    proxy_tcp_server.sendall(http_request)
    print("sent http request")

    http_response = proxy_tcp_server.recv(1024)
    http_response = http_response.decode("utf-8")
    print("got http response")

    proxy_tcp_server.close()
    print("closed tcp socket")
    return http_response


def get_ack(data1):
    if data1.decode("utf-8") != 'ack':
        print("error")
        return

    else:
        print("got ack - for receiving the html file")


def send_ack(address1):
    data = 'ack'
    # encoding the data
    data = data.encode()
    # send the ack back to the client
    proxy_udp.sendto(data, address1)
    print("sent ack to client")


def ask_file(proxy_tcp, index):
    print("asking for file_" + index)

    http_request = "GET /index.html HTTP/1.1\r\nHost: file_" + index
    http_request = http_request.encode()

    proxy_tcp.sendall(http_request)
    print("sent http request for file_" + index)

    # getting the size of file_
    size_of_file = proxy_tcp.recv(1024)
    size_of_file = size_of_file.decode("utf-8")
    size_of_file = int(size_of_file)
    file = ''

    temp = proxy_tcp.recv(1024)
    temp = temp.decode("utf-8")
    temp = temp[len(temp) - size_of_file:len(temp)]
    file += temp

    while size_of_file != len(file):
        temp = proxy_tcp.recv(1024)
        temp = temp.decode("utf-8")
        file += temp

    proxy_tcp.close()
    print("closed tcp socket")
    return file


def send_fin_tcp(_socket):
    value = b"FIN"
    _socket.send(value, "FIN")
    print("Send FIN")


if __name__ == "__main__":
    counter = 0
    print("connecting to client")
    # using UDP protocol
    proxy_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # local host and port
    proxy_udp.bind((proxy_ip, proxy_sport))

    print("connecting to files server")
    proxy_tcp_files = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_files_address = (server_files, 30714)  # need to change the port
    proxy_tcp_files.connect(server_files_address)

    print("connecting to site server")
    proxy_tcp_site = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_site_address = (server_site, server_site_sport)
    proxy_tcp_site.connect(server_site_address)

    # the loop for receiving and sending the data
    print("hello I am the Proxy server - the actual app\n")
    while True:

        counter = counter + 1
        # receiving data
        data, address = proxy_udp.recvfrom(1024)
        print("got message from client")

        # decoding tha data
        data = data.decode("utf-8")

        if data == "stop":
            # sending ack for stopping
            send_ack(address)

            # send_fin_tcp(proxy_tcp_site)  # site server
            value = b"stop"
            proxy_tcp_site.send(value)
            proxy_tcp_files.send(value)
            print("Send FIN")

            # send_fin_tcp(proxy_tcp_files)  # files server

            print("Client has been successfully disconnected")
            break

        # print for check
        print("The data: ", data)

        send_ack(address)

        # ######################################################################################################################

        # want to go to server that holds the site - now tcp connection

        resp = Connection_with_server_site(proxy_tcp_site)

        # #####################################################################################################################

        # send the site to the client
        print("responding to client")
        resp = resp.encode()
        proxy_udp.sendto(resp, address)

        # receiving ack
        data, address = proxy_udp.recvfrom(1024)
        get_ack(data)

        # receiving which file the client wants
        data, address = proxy_udp.recvfrom(1024)
        data = data.decode("utf-8")
        print("got the 'which file' request")

        # need to send ack for getting request for a file
        send_ack(address)
        print("chosen file is " + data)
        file = None

        if data == "file_1":
            file = ask_file(proxy_tcp_files, '1')
        elif data == "file_2":
            file = ask_file(proxy_tcp_files, '2')
        elif data == "file_3":
            file = ask_file(proxy_tcp_files, '3')
        else:
            print("error")
            print("somehow im here")
        print(file)
        # need to send the file to the client and get ack for it
        if file is None:
            print("wrong file request input")
            continue

        print("sending " + data + " to client")

        # CC!!!!!!!!!!!!!!!!!
        temp = len(file).to_bytes(32, 'big')
        proxy_udp.sendto(temp, address)  # sending the size of file
        packets_amount = len(file) / 1024
        packets = []
        for i in range(0, int(packets_amount)+1):  # splitting the file into packet size chunks
            chunk_of_file = file[i * 1024: 1024 + 1024 * i]
            tmp = [i+1, chunk_of_file, 0]
            packets.append(tmp)

        index = 0
        window_size = 1
        current_ack = 1
        suppose_to_ack = 1
        tmp = 0
        proxy_udp.settimeout(3)
        while index < packets_amount:  # The CC
            tmp = 0
            while window_size > tmp and index < packets_amount:
                packets[index][2] = window_size
                to_send = pickle.dumps(packets[index])
                index += 1
                proxy_udp.sendto(to_send, address)
                time.sleep(1)
                suppose_to_ack += 1
                tmp += 1

            tmp = 0
            while window_size > tmp and index < packets_amount:
                ack_sequence, address = proxy_udp.recvfrom(1024)
                ack_sequence = ack_sequence.decode("utf-8")
                if current_ack != ack_sequence[len(ack_sequence) - 1:len(ack_sequence)]:
                    continue
                else:
                    current_ack += 1

                tmp += 1
            if suppose_to_ack != current_ack:
                window_size = 1
                index = current_ack

            else:
                window_size *= 2
                index = current_ack

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        proxy_udp.settimeout(None)
        print("finish " + counter.__str__() + " task")

    # close the socket
    proxy_udp.close()
    print("---Successfully closed the socket")