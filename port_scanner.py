import socket
import ipaddress
from common_ports import ports_and_services  # Importing port-to-service dictionary

def get_open_ports(target, port_range, verbose=False):
    try:
        # Validate and resolve the target
        try:
            ip = ipaddress.ip_address(target)  # Check if it's a valid IP
            hostname = None
        except ValueError:
            # If not an IP, check if it's a valid hostname
            try:
                hostname = target
                ip = socket.gethostbyname(hostname)
            except socket.gaierror:
                # If hostname resolution fails, ensure clear error messages
                if any(char.isdigit() for char in target):  # Assumes it's an IP
                    return "Error: Invalid IP address"
                return "Error: Invalid hostname"
        
        # Scan the specified ports
        open_ports = []
        for port in range(port_range[0], port_range[1] + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((str(ip), port))
                if result == 0:
                    open_ports.append(port)

        if verbose:
            # Format verbose output
            if hostname is None:
                try:
                    hostname = socket.gethostbyaddr(str(ip))[0]
                except socket.herror:
                    hostname = str(ip)
                if hostname == str(ip):
                    result = f"Open ports for {ip}\nPORT     SERVICE\n"
                else:
                    result = f"Open ports for {hostname} ({ip})\nPORT     SERVICE\n"
            else:
                result = f"Open ports for {hostname} ({ip})\nPORT     SERVICE\n"
            for port in open_ports:
                service = ports_and_services.get(port, "unknown")
                result += f"{port:<8} {service}\n"
            return result.strip()
        else:
            return open_ports

    except ValueError:
        return "Error: Invalid IP address"
