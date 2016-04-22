"""UDP Client."""
import socket
import optparse


def main():
    """Main function that allows send UDP packets."""
    parser = optparse.OptionParser(
        "Usage %prog -H <target_host> -p <target_port>")
    parser.add_option(
        '-H', dest='target_host', type='string', help='specify UDP host')
    parser.add_option(
        '-p', dest='target_port', type='int', help='specify UDP port')
    (options, args) = parser.parse_args()

    target_host = options.target_host
    target_port = options.target_port
    # create a socket object
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # send some data to the target
        client.sendto('AAABBBCCC', (target_host, target_port))
        data, addr = client.recvfrom(4096)
        print data
    except Exception, e:
        print e

if __name__ == "__main__":
    main()
