import socket

if __name__ == "__main__":

    # using UDP protocol
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # local host and port
    server.bind(("127.0.0.1", 20230))

    # the loop for receiving and sending the data
    print("Server is running...\n")
    while True:
        # receiving data
        data, address = server.recvfrom(1024)

        # decoding tha data
        data = data.decode("utf-8")

        if data == "stop":
            print("Client has been successfully disconnected")
            break

        # print for check
        print("The old data: ", data)

        # change the meassage to uppercase letters
        data = data.upper()

        # print for check
        print("The new data: ", data)

        # encoding the data
        data = data.encode()

        # send the data back to the client
        server.sendto(data, address)

    #close the socket
    server.close()
    print("---Successfully closed the socket")


