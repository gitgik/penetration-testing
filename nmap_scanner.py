"""This file uses python-nmap module to do a port scan on a given host.

A far much robust implementation of the SYN-ACK port scanner we created.
"""
import nmap
import optparse


def nmap_scan(targer_host, target_port):
    """A function to scan a given host on a given TCP port using nmap."""
    nmpscan = nmap.PortScanner()
    nmpscan.scan(targer_host, target_port)
    state = nmpscan[targer_host]['tcp'][int(target_port)]['state']
    print (
        " [*] " + targer_host + " tcp/" + target_port + " " + state)


def main():
    """Main program."""
    parser = optparse.OptionParser(
        'usage %program -H <host> -p <target port>')
    parser.add_option(
        '-H', dest='target_host', type='string',
        help='specify target host')
    parser.add_option(
        '-p', dest='target_port', type='string',
        help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    target_host = options.target_host
    target_ports = str(options.target_port).split(',')

    if (target_host is None) | (target_ports[0] is None):
        print parser.usage
        exit(0)

    for port in target_ports:
        nmap_scan(target_host, port)

if __name__ == '__main__':
    main()
