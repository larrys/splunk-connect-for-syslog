"""
simple syslog-ng Python parser example
resolves IP to hostname
value pair names are hard-coded
"""
import socket

try:
    import syslogng
    from syslogng import LogParser
except Exception:

    class LogParser:
        pass


class FixHostnameResolver(LogParser):
    def parse(self, log_message):
        """
        Resolves IP to hostname
        """

        # try to resolve the IP address
        try:
            ipaddr = log_message.get_as_str("SOURCEIP", "", repr="internal")

            hostname, _, _ = socket.gethostbyaddr(ipaddr)

            if hostname == ipaddr:
                return False

            parts = str(hostname).split(".")
            name = parts[0]
            if len(parts) > 1:
                log_message["HOST"] = name
        except Exception:
            return False

        # return True, other way message is dropped
        return True


class FixFQDNResolver(LogParser):
    def parse(self, log_message):
        """
        Resolves IP to FQDN
        """

        # try to resolve the IP address
        try:
            ipaddr = log_message.get_as_str("SOURCEIP", "", repr="internal")

            fqdn, _, _ = socket.gethostbyaddr(ipaddr)

            if fqdn == ipaddr:
                return False

            log_message["HOST"] = str(fqdn)
        except Exception:
            return False

        # return True, other way message is dropped
        return True
