import socket

if __name__ == "__main__":

    # using UDP protocol
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # the loop for receiving and sending the data
    print("Client is running...\n")
    while True:

        # receiving data from user
        data = input("pls enter a sentence: ")
        print("\n")

        #option for closing the socket
        if data == "stop":
            data = data.encode("utf-8")
            client.sendto(data, ("127.0.0.1", 20230))

            print("---The client has successfully diconected from the server")
            break

        # encoding the data
        data = data.encode()

        # send the data to the server
        client.sendto(data, ("127.0.0.1", 20230))

        # receiving data from the server
        data, addr = client.recvfrom(1024)

        # decoding tha data
        data = data.decode("utf-8")

        # print the data we have got from the server
        print("The new data: ", data)
        print("\n")

    # close the socket
    client.close()
    print("---Successfully closed the socket")







