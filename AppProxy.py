from socket import *
from scapy.all import *


#------Magic Numbers-------#
proxy_sport = 20230
proxy_ip = '127.0.0.1'
server_site_sport = 80
server_site = '127.0.0.1'
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
    print(http_response.decode("utf-8"))
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
        # resp = resp.encode()
        porxy_udp.sendto(resp, address)


        # receiving ack
        data, address = porxy_udp.recvfrom(1024)

        get_ack(data)








        print("finish!!!")
        break





    #close the socket
    porxy_udp.close()
    print("---Successfully closed the socket")
