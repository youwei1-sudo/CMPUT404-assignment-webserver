#  coding: utf-8 
import socketserver
from os import path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/



class MyWebServer(socketserver.BaseRequestHandler):
    def body_response(self, words):
        """
        text in 404 HTML response body .
        """
        return (f"""
        <!DOCTYPE HTML>
        <html>
        <body>
            <h1>{words} </h1>
        </body>
        </html>
        """)


    def gen_response(self,c_path,message,status_code, root_flag = False):
        """
        Returns the http header according to the imput status code 
        """
        if (status_code == "200") :
            if root_flag:
                f = open(c_path + "index.html", "r")
                data = f.read()
                message = message + "\r\n"
                message = message + data
            else:
                f = open(c_path, "r")
                data = f.read()
                message = message + "\r\n"
                message = message + data
            
        elif (status_code == "301") :
            f = open(c_path + "index.html", "r")
            data = f.read()
            message = message + "Location: " + c_path + "\r\n"
            message = message + data
            
        elif (status_code == "404") :
            message = message + "\r\n"
            message = message + self.body_response("404 NOT FOUND, COOL")
            
        elif (status_code == "405") :
            message = message + "\r\n"
            message = message + self.body_response("405,PLEASE, DONT USE THIS METHOD")
        return message


    def handle(self):
        """
        handle request
        """
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        print("gota self.data, the request")
        # split byte recievd to readable format
        method_path_protocol = (self.data.decode("utf-8").split('\n'))[0].strip().split()
        print(method_path_protocol)
        rest = ""
        root_flag = False
        if (method_path_protocol[0] == "GET") :
            c_path = "www"+ method_path_protocol[1]
            if (path.exists(c_path)):
                if (path.isdir(c_path)):
                    if (c_path[-1] == "/"):
                        status_code = "200"
                        rest = " OK"
                        root_flag = True
                    else:
                        status_code = "301"
                        c_path = c_path + "/"
                        rest = " Moved Permanently"
                elif (path.isfile(c_path)) :
                    status_code = "200"
                    rest = " OK"
            else :
                status_code = "404"
                rest = " Not Found"
        else:
            # if it is not get
            status_code = "405"
            rest = " Method Not Allowed"

        message = method_path_protocol[2] + " " + status_code + rest + "\r\n"
        response_data = self.gen_response(c_path , message, status_code, root_flag)
        self.request.sendall(bytearray(response_data,'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
