"""First things first.

Reconnaissance: An attacker discover where the vulnerabilities
are before selecting the exploits for a target.
this program scans for open TCP ports.
It sends TCP SYN packets to a series of ports and waits for
TCP ACK response. (full three-way handshake)
"""

import optparse
from threading import Thread, Semaphore
from socket import *

# Semaphore to prevent threads from outputing to screen at the same time
screenlock = Semaphore(value=1)


def connection_scan(target_host, target_port):
    """A function that resolves the IP to connect to the target host."""
    try:
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        tcp_socket.connect(target_host, target_port)
        tcp_socket.send('Python in action\r\n')
        results = tcp_socket.recv(100)
        screenlock.acquire()
        print ('[+] %d/tcp open' % target_port)
        print('[+]' + str(results))
    except:
        screenlock.acquire()
        print ('[-] %d/tcp closed' % target_port)
    finally:
        screenlock.release()
        tcp_socket.close()


def port_scan(target_host, target_ports):
    """A function that scans for open ports on a connected host."""
    try:
        target_ip = gethostbyname(target_host)
    except:
        print ("[-] Cannot resolve '%s': Unkwown host" % target_host)
        return

    try:
        target_name = gethostbyaddr(target_ip)
        print ('\n[+] Scan results for: ' + target_name[0])
    except:
        print ('\n[+] Scan results for: ' + target_ip)
    setdefaulttimeout(1)

    for port in target_ports:
        # spawn a thread for each port scan
        print('Scanning port: ' + port)
        thread = Thread(
            target=connection_scan, args=(target_host, int(port)))
        thread.start()


def main():
    """Main function that calls the port scan utility."""
    parser = optparse.OptionParser('usage %prog -H <host> -p <target port>')
    parser.add_option(
        '-H', dest='target_host', type='string',
        help="specify target host"
    )
    parser.add_option(
        '-p', dest="target_port", type='string',
        help='specify target port[s] separated by a comma')

    (options, args) = parser.parse_args()
    target_host = options.target_host
    target_ports = str(options.target_port).split(',')
    if (target_host is None) | (target_ports[0] is None):
        print ('[-] Please specify a target host and port[s].')
        print (parser.usage)
        exit(0)
    port_scan(target_host, target_ports)

if __name__ == '__main__':
    main()
