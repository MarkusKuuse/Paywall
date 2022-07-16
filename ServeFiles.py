from Lib.http import server
import socketserver

Port = 8080
Handler = server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", Port), Handler)
print("serving at port: ", Port)
httpd.serve_forever()


