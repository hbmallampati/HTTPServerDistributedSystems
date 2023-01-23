import socket
import os
import threading
import sys
import argparse
import time
import signal
import builtins



HOST = "localhost"
PORT = 8000 #default
SERVER_DIR = './' #default


def Serverlistener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))

        while True:
            sock.listen()
            conn, addr = sock.accept()

            t = threading.Thread(target=keepalive, args=(conn, addr))
            t.start()



def keepalive(conn, address):
    size = 1024
    with conn:
        conn.settimeout(4)

        while True:
            try:
                request = conn.recv(size).decode()
                headers = request.split('\r\n')
                REST  = headers[0].split()

                if REST[0] == "GET":
                    HtttpConnectionWorkerThread(REST, conn)

            except Exception as e:
                break

    conn.close()



def HtttpConnectionWorkerThread(request, conn):
    print("Client request : ")
    print(request)

    if(request[1] == '/'):
        request[1] = '/index.html'
    try:
        if(request[1].find('.html') > 0):
            filename = SERVER_DIR + request[1]

            with open(filename,  'r', encoding='latin-1') as f:
                content = f.read()

            f.close()

            response = str.encode("HTTP/1.1 200 OK\n")
            response = response + str.encode('Content-Type: text/html\n')
            response = response + str.encode('\r\n')

            
            conn.sendall(response)
            conn.sendall(content.encode())
        

        elif(request[1].find('.png') > 0): 
            image_type = request[1].split('.')[1]

            filename = '.' + request[1]
            image_data = open(filename, 'rb')

            response = str.encode("HTTP/1.1 200 OK\n")
            image_type = "Content-Type: image/" + image_type +"\r\n"

            response = response + str.encode(image_type)
            response = response + str.encode("Accept-Ranges: bytes\r\n\r\n")

            conn.sendall(response)
            conn.sendall(image_data.read())


        elif(request[1].find('.jpeg') > 0): 
            image_type = request[1].split('.')[1]

            filename = '.' + request[1]
            image_data = open(filename, 'rb')

            response = str.encode("HTTP/1.1 200 OK\n")
            image_type = "Content-Type: image/" + image_type +"\r\n"

            response = response + str.encode(image_type)
            response = response + str.encode("Accept-Ranges: bytes\r\n\r\n")

            conn.sendall(response)
            conn.sendall(image_data.read())

        
        elif(request[1].find('.jpg') > 0):
            image_type = request[1].split('.')[1]

            filename = '.' + request[1]
            image_data = open(filename, 'rb')

            response = str.encode("HTTP/1.1 200 OK\n")
            image_type = "Content-Type: image/" + image_type +"\r\n"

            response = response + str.encode(image_type)
            response = response + str.encode("Accept-Ranges: bytes\r\n\r\n")

            conn.sendall(response)
            conn.sendall(image_data.read())


        elif(request[1].find('.gif') > 0):
            gif_type = request[1].split('.')[1]

            filename = '.' + request[1]
            gif_data = open(filename, 'rb')

            response = str.encode("HTTP/1.1 200 OK\n")
            gif_type = "Content-Type: image/" + gif_type +"\r\n"

            response = response + str.encode(gif_type)
            response = response + str.encode("Accept-Ranges: bytes\r\n\r\n")

            conn.sendall(response)
            conn.sendall(gif_data.read())


        else:
            conn.sendall(str.encode("HTTP/1.1 400 BAD REQUEST\r\nBad Request"))

    except FileNotFoundError:
        conn.sendall(str.encode("HTTP/1.1 404 NOT FOUND\r\nFile Not Found"))

    except PermissionError:
       conn.sendall(str.encode("HTTP/1.1 403 FORBIDDEN\r\nForbidden"))

    except Exception:
        conn.sendall(str.encode("HTTP/1.1 500 Internal Server Error\r\nInternal Server Error"))




if __name__ == "__main__":

    inputArgs = argparse.ArgumentParser()
    inputArgs.add_argument('-document_root', type=str)
    inputArgs.add_argument('-port', type=int)
    parsedArgs = inputArgs.parse_args()

    try:
        PORT = parsedArgs.port
        SERVER_DIR = parsedArgs.document_root

    except AttributeError:
        print("Arguments are missing or input type is wrong")
        print("Input type = python ./server.py -document_root './' -port 8000")
        sys.exit(1)

    print("Server host and port" + HOST + ":" + str(PORT))
    print("Server directory:" + SERVER_DIR)
    Serverlistener()