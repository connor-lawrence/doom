import wifi, socket, screen

server = None
server_status = False

bar = "off"

def handle_request(request):
    global bar
    if request == "/red": bar = "red"
    elif request == "/yellow": bar = "yellow"
    elif request == "/green": bar = "green"
    elif request == "/cyan": bar = "cyan"
    elif request == "/blue": bar = "blue"
    elif request == "/magenta": bar = "magenta"
    elif request == "/white": bar = "white"
    elif request == "/bright": bar = "bright"
    elif request == "/off": bar = "off"
    elif request == "/min": screen.brightness = 4/9
    elif request == "/down" and screen.brightness > 0.5: screen.brightness /= 1.5
    elif request == "/normal": screen.brightness = 1
    elif request == "/up" and screen.brightness < 5: screen.brightness *= 1.5
    elif request == "/max": screen.brightness = 5.0625

def webpage():
    return """\
HTTP/1.1 200 OK

<html>
    <head>
        <!-- <meta http-equiv="refresh" content="1"> -->
        <title>Doom_Grid</title>
        <style>
            body {
                background-color: black;
                color: white;
                font-family: monospace;
                font-size: 3rem;
                padding: 64px;
            }

            /* ----- Element Defaults ----- */

            button, input, select, textarea {
                background-color: black;
                color: white;
                font-family: monospace;
                font-size: 3rem;
                border: 3px solid deepskyblue;
                border-radius: 15px;
                padding: 24px 24px;
                transition: background 0.2s ease, color 0.2s ease, border 0.2s ease;
            }

            button::placeholder, input::placeholder, select::placeholder, textarea::placeholder {color: silver;}

            /* ----- Element Actions ----- */

            button:hover, input:hover, select:hover, textarea:hover {
                background-color: deepskyblue;
                color: black;
                border: 3px solid black;
                transition: background 0.2s ease;
            }

            a {color: skyblue; text-decoration: none;}

            a:hover {color: white; font-weight: bold;}

            button:hover, select:hover, a:hover {cursor: pointer;}

            input:hover::placeholder, select:hover::placeholder, textarea:hover::placeholder {color: black;}

            input:focus, select:focus, textarea:focus {
                background-color: black;
                color: deepskyblue;
                border: 3px solid deepskyblue;
                transition: background 0.2s ease;
            }

            input:focus::placeholder, select:focus::placeholder, textarea:focus::placeholder {color: black;}

            button:active {
                background-color: black;
                color: white;
                border: 3px solid deepskyblue;
                transition: background 0s ease;
            }

        </style>
    </head>
    <body>
        <h1>Doom_Grid</h1>
        <p style="height: 1px;"></p>
        <p>Set Bar Color:</p>
        <button onclick="send('/red')">Red</button>
        <button onclick="send('/yellow')">Yellow</button>
        <button onclick="send('/green')">Green</button><br><br>
        <button onclick="send('/cyan')">Cyan</button>
        <button onclick="send('/blue')">Blue</button>
        <button onclick="send('/magenta')">Magenta</button><br><br>
        <button onclick="send('/white')">White</button>
        <button onclick="send('/bright')">Bright</button>
        <button onclick="send('/off')">OFF</button>
        <p style="height: 1px;"></p>
        <p>Change Screen Brightness:</p>
        <button onclick="send('/min')">Low</button>
        <button onclick="send('/normal')">Normal</button>
        <button onclick="send('/max')">Max</button><br><br>
        <button onclick="send('/down')">Down</button>
        <button onclick="send('/up')">Up</button>
        <br>
        <script>
            function send(path) {
                fetch(path);
            }
    </script>
    </body>
</html>
"""

def host():
    global server_status, server
    address = ('0.0.0.0', 80)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try: s.bind(address)
    except Exception as error:
        print("Error opening server:", error)
        return
    s.listen(1)
    s.settimeout(0.0001)
    server_status = True
    server = s
    print("Server running at", wifi.wifi_ip, "port 80...")

def server_loop():
    if not server_status: return
    try: connection, address = server.accept()
    except OSError: return
    try:
        request = connection.recv(1024).decode()
        path = request.split(' ')[1]
        handle_request(path)
        connection.send(webpage())
    finally: connection.close()

def close(s):
    global server_status, server
    server_status = False
    try: s.shutdown(socket.SHUT_RDWR)
    except: pass
    try: s.close()
    except Exception as error: print("Error closing server:", error)
    print("Server closed")
    server = None