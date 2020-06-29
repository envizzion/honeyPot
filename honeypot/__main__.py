"""NanoPot.

Simple TCP honeypot logger

Usage:
  nanopot <config_filepath>

Options:
  <config_filepath>     Path to config options .ini file
  -h --help             Show this screen.
"""
import configparser
import sys

import logging
import threading
from socket import socket, timeout
from emaill import Email 


class HoneyPot(object):

    def __init__(self, bind_ip, ports, log_filepath,mailer):
        if len(ports) < 1:
            raise Exception("No ports provided.")

        self.bind_ip = bind_ip
        self.ports = ports
        self.log_filepath = log_filepath
        self.listener_threads = {}
        self.logger = self.prepare_logger()
        self.mailer=mailer

        # self.logger.info("Honeypot initializing...")
        # self.logger.info("Ports: %s" % self.ports)
        # self.logger.info("Log filepath: %s" % self.log_filepath)

    def handle_connection(self, client_socket, port, ip, remote_port):
        self.logger.info("Connection %s %s %d null" % (port, ip, remote_port))

        client_socket.settimeout(10)
        try:
            data = client_socket.recv(64)
            self.logger.info("Data %s %s %d %s" % (port, ip, remote_port, data))
            client_socket.send("Access denied.\n".encode('utf8'))
            self.mailer.sendMessage(port,ip,remote_port,data)

        except timeout:
            pass
        client_socket.close()

    def start_new_listener_thread(self, port):
        # Create a new listener
        listener = socket()  # Defaults (socket.AF_INET, socket.SOCK_STREAM)
        listener.bind((self.bind_ip, int(port)))
        listener.listen(5)
        while True:
            client, addr = listener.accept()
            client_handler = threading.Thread(target=self.handle_connection, args=(client, port, addr[0], addr[1]))
            client_handler.start()

    def start_listening(self):
        for port in self.ports:
            self.listener_threads[port] = threading.Thread(target=self.start_new_listener_thread, args=(port,))
            self.listener_threads[port].start()

    def run(self):
        self.start_listening()

    def prepare_logger(self):
        
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S.%03d',
                           
                          #  datefmt='YYYY/MM/DD HH:mm:ss.SSS',
                            filename=self.log_filepath,
                            filemode='w')
        logger = logging.getLogger(__name__)
        
        # Adding console handler
        # Adding console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        return logger


class ArrowTimeFormatter(logging.Formatter):

    def formatTime(self, record, datefmt=None):
        arrow_time = Arrow.fromtimestamp(record.created)

        if datefmt:
            arrow_time = arrow_time.format(datefmt)

        return str(arrow_time)



print(len(sys.argv))
# Check arguments
if  len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
    print(__doc__)
    sys.exit(1)

# Load config
config_filepath ="honeypot.ini"
print(config_filepath)
config = configparser.ConfigParser()
config.read(config_filepath)

ports = config.get('default', 'ports', raw=True, fallback="8080,8888,9999")
host = config.get('default', 'host', raw=True, fallback="0.0.0.0")
# log_filepath = config.get('default', 'logfile', raw=True, fallback="/var/log/nanopot.log")
log_filepath = config.get('default', 'logfile', raw=True, fallback="/var/honeypot/honeypot.log")
username =config.get('default', 'username', raw=True, fallback="none") 
password =config.get('default', 'password', raw=True, fallback="none") 
sender = config.get('default', 'sender', raw=True, fallback="HoneyPot Watchman") 
targets = config.get('default', 'targets', raw=True, fallback="none") 


# Double check ports provided
ports_list = []
targets_list=[]
try:
    ports_list = ports.split(',')
    targets_list=targets.split(",")
except Exception as e:
    print('[-] Error parsing ports: %s.\nExiting.', ports)
    sys.exit(1)


#email initialize 

mailer=Email(username,password,sender,targets_list)


# Launch honeypot
honeypot = HoneyPot(host, ports_list, log_filepath,mailer)
honeypot.run()
