import time
import nets
import led
import wifi
import socketpool

server_status = "CLOSED"
routes = {}

pool = socketpool.SocketPool(wifi.radio)
server = pool.socket()
server.settimeout(0.1)
server.bind(("0.0.0.0", 80))
server.listen(1)



def route(path):
    def wrapper(function):
        routes[path] = function
        return function
    return wrapper

def handle_request(path, request):
    handler = routes.get(path)
    if handler: 
        return handler(request)
    return "404 Not Found"

@route("/")
def home(request):
    return f"""
<!DOCTYPE html>
    <head>
        <title>Doom_Stick</title>
        <style>
            body {{
                background-color: black;
                color: white;
                font-family: monospace;
                font-size: 3rem;
                padding: 20px 40px;
            }}
        </style>
    </head>
    <body>
        <h1>Doom_Stick</h1>
        <p style="height: 1px;"></p>
        <p>Board Status:</p>
        <ul>
            <li>Time: {time.monotonic()}</li>
            <li>LED1: {led.state}</li>
            <li>SSID: {nets.wifi_network}</li>
            <li>IPv4: {nets.wifi_ip}</li>
            <li>Srvr: {server_status}</li>
        </ul>
        <br>
    </body>
</html>
"""


@route("/refresh")
def home(request):
    return f"""
<!DOCTYPE html>
    <head>
        <meta http-equiv="refresh" content="1">
        <title>Doom_Stick/Refresh</title>
        <style>
            body {{
                background-color: black;
                color: white;
                font-family: monospace;
                font-size: 3rem;
                padding: 20px 40px;
            }}
        </style>
    </head>
    <body>
        <h1>Doom_Stick</h1>
        <p style="height: 1px;"></p>
        <p>Board Status:</p>
        <ul>
            <li>Time: {time.monotonic()}</li>
            <li>LED1: {led.state}</li>
            <li>SSID: {nets.wifi_network}</li>
            <li>IPv4: {nets.wifi_ip}</li>
            <li>Srvr: {server_status}</li>
        </ul>
        <br>
    </body>
</html>
"""

def open_server():
    global server_status
    server_status = "OPEN"
    print("Server open on", nets.wifi_network, "at", nets.wifi_ip, "Port 80...")
    while server_status == "OPEN":
        try:
            connection, address = server.accept()
            handle_connection(connection)
        except OSError: pass


def handle_connection(connection):
    try:
        buffer = bytearray(1024)
        bytes_read = connection.recv_into(buffer)
        
        if bytes_read <= 0:
            return
        
        request = buffer[:bytes_read].decode("utf-8", "ignore")
        if not request: 
            return

        line = request.split("\r\n", 1)[0]
        parts = line.split()
        path = parts[1] if len(parts) > 1 else "/"

        body = handle_request(path, request)

        response = ("HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    "Connection: close\r\n\r\n" + body)

        connection.send(response.encode("utf-8"))
        led.blink_led(1, 0.1)
    
    finally:
        connection.close()