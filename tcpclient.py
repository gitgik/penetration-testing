"""A minimalist TCP client."""
import socket
import optparse

def main():
    """Main function."""

    # specify the options needed to run the program
    parser = optparse.OptionParser(
        "usage %prog -H <target_host> -p <target_port>")
    parser.add_option(
        '-H', dest="target_host", type='string', help="specify target host")
    parser.add_option(
        '-p', dest="target_port", type='int', help="specify target port")
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    (options, args) = parser.parse_args()

    target_host = options.target_host
    target_port = options.target_port

    try:
        client.connect((target_host, target_port))
        # Send some data to the target host
        client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
        response = client.recv(4096)
        print response
        client.close()
    except Exception, e:
        print "ERROR OCCURED: "
        print e

if __name__ == '__main__':
    main()
