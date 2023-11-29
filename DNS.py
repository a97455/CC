import dns.resolver
import subprocess
import time

def get_host_by_name(name):
    zone = "cc"
    full_name = f"{name}.{zone}"

    try:
        result = dns.resolver.resolve(full_name, 'A')
        return result[0].address
    except Exception as e:
        print(e)


def start_named_server():
    try:
        # Check if the named process is running
        subprocess.check_output(["pidof", "named"])
    except subprocess.CalledProcessError:
        # If named is not running, start it
        subprocess.run(["sudo", "/sbin/named", "-c", "/etc/bind/named.conf"])
        # Wait for a moment to let the server start (you might need to adjust this)
        time(2)