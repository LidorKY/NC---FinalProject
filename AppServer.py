import socket

server_site_sport = 80

server_site = '127.0.0.1'



if __name__ == "__main__":

    print("Hello I am the server that has the site\n")

    server_site_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_site_tcp.bind((server_site, server_site_sport))

    server_site_tcp.listen(1)
    print("listening...\n")

    ans_socket, ans_addr = server_site_tcp.accept()

    request = ans_socket.recv(1024).decode()

    print("got http request\n")

    http_response = b"HTTP/1.1 200 OK\r\nContent_Type: text/html\r\n\r\n    <Html><Head><title>Example of make a text B,I,U</title></Head><Body><b> [This text is Bold......] </b><I> [This text is Italic......] </I><U> [This text is Underline......] </U></Body></Html>"

    ans_socket.sendall(http_response)

    print("sent http response\n")

    ans_socket.close()
    print("closed socket...\n")
    print("finished!!!")






