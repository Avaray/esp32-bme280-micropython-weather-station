# Issues: 
# Captive Portal is not opening on Samsung phone (A51). Does Samsung require SSL?

print('\nRunning Admin Mode code. This code is not finished yet.\n')

import gc
import network
import sys
import uasyncio as asyncio
import usocket as socket
import ustruct as struct

import config

# Access Point settings
SERVER_SSID = config.ADMIN_MODE_WIFI_SSID if config.ADMIN_MODE_WIFI_SSID else 'Weather Station'
SERVER_AUTHMODE = network.AUTH_OPEN if not config.ADMIN_MODE_WIFI_PASSWORD else network.AUTH_WPA_WPA2_PSK
SERVER_IP = '10.0.0.1'
SERVER_SUBNET = '255.255.255.0'


def wifi_start_access_point():
    wifi = network.WLAN(network.AP_IF)
    wifi.active(True)
    wifi.ifconfig((SERVER_IP, SERVER_SUBNET, SERVER_IP, SERVER_IP))
    wifi.config(essid=SERVER_SSID, authmode=SERVER_AUTHMODE)
    print('Network config:', wifi.ifconfig())


def _handle_exception(loop, context):
    """ uasyncio v3 only: global exception handler """
    print('Global exception handler')
    sys.print_exception(context["exception"])
    sys.exit()


class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.domain = ''
        tipo = (data[2] >> 3) & 15  # Opcode bits
        if tipo == 0:  # Standard query
            ini = 12
            lon = data[ini]
            while lon != 0:
                self.domain += data[ini + 1:ini + lon + 1].decode('utf-8') + '.'
                ini += lon + 1
                lon = data[ini]
        print("DNSQuery domain:" + self.domain)

    def response(self, ip):
        print("DNSQuery response: {} ==> {}".format(self.domain, ip))
        if self.domain:
            packet = self.data[:2] + b'\x81\x80'
            packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'  # Questions and Answers Counts
            packet += self.data[12:]  # Original Domain Name Question
            packet += b'\xC0\x0C'  # Pointer to domain name
            packet += b'\x00\x01\x00\x01\x00\x00\x00\x3C\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
            packet += struct.pack('!4B', *[int(x) for x in ip.split('.')])  # 4 bytes of IP
        return packet


def get_file_content(file_path):
    """ Function to read a file from the /web directory """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except OSError:
        return None


class MyApp:
    async def start(self):
        # Get the event loop
        loop = asyncio.get_event_loop()

        # Add global exception handler
        loop.set_exception_handler(_handle_exception)

        # Start the wifi AP
        wifi_start_access_point()

        # Create the server and add task to event loop
        await asyncio.start_server(self.handle_http_connection, "0.0.0.0", 80)

        # Start the DNS server task
        loop.create_task(self.run_dns_server())

        # Start looping forever
        print('Looping forever...')
        await loop.run_forever()

    async def handle_http_connection(self, reader, writer):
        gc.collect()

        # Get HTTP request line
        data = await reader.readline()
        request_line = data.decode()
        addr = writer.get_extra_info('peername')
        print('Received {} from {}'.format(request_line.strip(), addr))

        # Read headers
        while True:
            gc.collect()
            line = await reader.readline()
            if line == b'\r\n':
                break

        # Handle the request
        if len(request_line) > 0:
            try:
                path = request_line.split(' ')[1]
            except IndexError:
                path = '/'

            # https://github.com/NickSto/uptest/blob/master/captive-portals.md
            # https://github.com/tripflex/captive-portal?tab=readme-ov-file#known-endpoints
            # https://en.wikipedia.org/wiki/Captive_portal
            captive_portal_urls = [
                '/',
                '/check_network_status.txt',
                '/connecttest.txt',
                '/gen_204',
                '/generate_204', 
                '/hotspot-detect.html',
                '/hotspot-detect.html', 
                '/hotspotdetect.html',
                '/kindle-wifi/wifiredirect.html',
                '/library/test/success.html',
                '/mobile/status.php',
                '/ncsi.txt', 
                '/success.html', 
                '/success.txt',
            ]

            # TODO
            # I'm thinking about redirect all requests to the captive portal, except the ones that are for the web server files
            # List of files is available to get using utils.getProjectFilesList() function
            # files = utils.getProjectFilesList().['web']
                    
            # Serve captive portal redirect
            if path in captive_portal_urls:
                response = "HTTP/1.0 302 Found\r\nLocation: http://10.0.0.1/index.html\r\n\r\n"
                await writer.awrite(response)
            else:
                # Serve static files
                if path == '/':
                    path = '/index.html'  # Default file to serve

                file_path = '/web' + path
                try:
                    with open(file_path, 'r') as file:
                        await writer.awrite("HTTP/1.0 200 OK\r\n\r\n")
                        while True:
                            chunk = file.read(1024)
                            if not chunk:
                                break
                            await writer.awrite(chunk)
                except OSError:
                    missing_content = get_file_content('/web/404.html')
                    if missing_content:
                        response = "HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n" + missing_content
                    else:
                        response = "HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
                        response += "<html><head><title>404 Not Found</title><body>File not found</body></html>"
                    await writer.awrite(response)

        # Close the socket
        await writer.aclose()

    # Function to handle incoming DNS requests
    async def run_dns_server(self):
        udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udps.setblocking(False)
        udps.bind(('0.0.0.0', 53))

        while True:
            try:
                await asyncio.sleep(0)  # Yield control to ensure non-blocking behavior
                try:
                    data, addr = udps.recvfrom(4096)
                    print("Incoming DNS request...")

                    DNS = DNSQuery(data)
                    udps.sendto(DNS.response(SERVER_IP), addr)

                    print("Replying: {:s} -> {:s}".format(DNS.domain, SERVER_IP))
                except OSError as e:
                    if e.errno != 11:  # EAGAIN
                        raise
            except Exception as e:
                print("DNS server error:", e)
                await asyncio.sleep_ms(3000)

        udps.close()


# Main code entrypoint
try:
    myapp = MyApp()
    asyncio.run(myapp.start())
except KeyboardInterrupt:
    print('Interrupted with keyboard')
finally:
    asyncio.new_event_loop()  # Clear retained state
