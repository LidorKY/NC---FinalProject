import socket

# ------Magic Numbers-------#
server_site_sport = 80
server_site_ip = '127.0.0.1'
server_site_address = (server_site_ip, server_site_sport)
# --------------------------#




if __name__ == "__main__":
    #----opening socket----#
    print("Hello I am the server that has the site\n")
    server_site_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_site_tcp.bind(server_site_address)
    server_site_tcp.listen(1)
    print("listening...\n")
    #----------------------#

    #----client connects + receiving request + sending response----#
    ans_socket, ans_addr = server_site_tcp.accept()
    request = ans_socket.recv(8192).decode("utf-8")
    temp = request.find("site.html")
    if temp != -1:
        print("got http request\n")
        #cannot copy the html site from the file
        http_response = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" \
                        b"<Html>" \
                        b"<Head>" \
                        b"<title>" \
                        b"Lidor and Gal" \
                        b"</title>" \
                        b"</Head>" \
                        b"<Body>" \
                        b"<style>" \
                        b"body" \
                        b"{" \
                        b"background-image: url('main.jpeg');" \
                        b"background-repeat: no-repeat;" \
                        b"background-attachment: fixed;" \
                        b"background-size: cover;" \
                        b"}" \
                        b"</style>" \
                        b"<h1> <p>hello dear user and welcome to our site</p> </h1>" \
                        b"<a href= first_image.jpg>" \
                        b"<p><b>if you want to get the file 'image1.jpg' press here </b></p>" \
                        b"<a href= second_image.jpg>" \
                        b"<p><b>if you want to get the file 'image2.jpg' press here </b></p>" \
                        b"<a href= third_image.jpg>" \
                        b"<p><b>if you want to get the file 'image3.jpg' press here </b></p>" \
                        b"</Body>" \
                        b"</Html>"
        ans_socket.send(http_response)
        print("sent http response to the proxy\n")


    ans_socket.close()
    print("closed socket...\n")
    print("finished!!!")