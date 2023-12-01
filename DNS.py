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
        with open("/dev/null", "w") as null_file:
            subprocess.run(
                ["sudo", "/sbin/named", "-c", "/etc/bind/named.conf"],
                stdout=null_file,
                stderr=null_file
            )
        # Wait for a moment to let the server start (you might need to adjust this)
        time.sleep(2)
