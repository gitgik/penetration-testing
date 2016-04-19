"""An anonymous FTP login."""
import ftplib


def anonymous_login(hostname):
    """Anonymously login on ftp."""
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print '\n[*] ' + str(hostname) + 'ftp anonymous login succeeded'
        ftp.quit()
        return True
    except Exception, e:
        print e
        print '\n[-] ' + str(hostname) + 'FTP anonymous login failed'
        return False
    host = '192.168.8.1'
    anonymous_login(host)
