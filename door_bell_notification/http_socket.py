import socket
from wlan import WLAN

def createSocket(callback):
    wlan = WLAN()
    # Set up server parameters
    HOST = wlan.getLocalIp()  # IP address of the Raspberry Pi Pico
    PORT = 8080      # Port number to listen for incoming connections

    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    
    print('Waiting for incoming connections... http://' + HOST + ':' + str(PORT))
    
    def listener():
        while True:
            try:
                conn, addr = s.accept()
                print('Connected by', addr)
                callback()
            except Error:
                print('Error', Error)
            
#             # Extract query parameters from URL
#             query_start = data_str.find('?')  # Find the start of query parameters
#             if query_start != -1:
#                 query_end = data_str.find(' ', query_start)  # Find the end of query parameters
#                 if query_end != -1:
#                     query_string = data_str[query_start + 1:query_end]  # Extract query string
#                     query_params = query_string.split('&')  # Split query parameters into a list
# 
#                     # Store query parameters in a dictionary
#                     query_dict = {}
#                     for param in query_params:
#                         key, value = param.split('=')  # Split key-value pairs
#                         query_dict[key] = value  # Add key-value pair to dictionary
# 
#                     # Access query parameters by key
#                     print('Query parameters:')
#                     callback(query_dict)
#                     # print('Key:', query_dict.get('dupa'))  # Access value by key using .get() method
# 
#             
#             # Process the received data as needed
#             # Send response back to the client, if required
            conn.close()
    
    return listener
