import subprocess
import requests
import socket
import statistics
from concurrent.futures import ThreadPoolExecutor

# ----------------
# Ping Test
# ----------------
def ping(ip):
    times = []

    for _ in range(4):
        r = subprocess.run(["ping","-c","1",ip],capture_output=True,text=True)

        if "time=" in r.stdout:
            t = float(r.stdout.split("time=")[1].split(" ")[0])
            times.append(t)

    if times:
        avg = statistics.mean(times)
        print(f"✅ {ip} Online | Avg Ping: {round(avg,2)} ms")
        return avg
    else:
        print(f"❌ {ip} Offline")
        return None


# ----------------
# IP Info
# ----------------
def ip_info(ip):

    try:
        data = requests.get(f"http://ip-api.com/json/{ip}").json()

        print("\nIP INFO")
        print("Country:",data.get("country"))
        print("City:",data.get("city"))
        print("ISP:",data.get("isp"))
        print("Org:",data.get("org"))

    except:
        print("Error getting info")


# ----------------
# Port Scan
# ----------------
def port_scan(ip):

    ports = [21,22,25,53,80,110,139,143,443,445,3306,3389]

    print("\nScanning Ports...\n")

    for port in ports:

        s = socket.socket()
        s.settimeout(1)

        if s.connect_ex((ip,port)) == 0:
            print("✅ Open:",port)

        s.close()


# ----------------
# Clean IP Finder
# ----------------
def check_ip(ip):

    r = subprocess.run(["ping","-c","1",ip],stdout=subprocess.DEVNULL)

    if r.returncode == 0:
        print("✅ Clean IP:",ip)

        with open("clean_ips.txt","a") as f:
            f.write(ip+"\n")


def find_clean(base):

    print("\nScanning...\n")

    with ThreadPoolExecutor(max_workers=200) as ex:

        for i in range(1,255):

            ip = f"{base}.{i}"
            ex.submit(check_ip,ip)


# ----------------
# Range Scan
# ----------------
def scan_range(base,start,end):

    for i in range(start,end+1):

        ip = f"{base}.{i}"

        r = subprocess.run(["ping","-c","1",ip],stdout=subprocess.DEVNULL)

        if r.returncode == 0:
            print("Online:",ip)


# ----------------
# Menu
# ----------------
while True:

    print("\n====== MAHAN IP TOOL ======")
    print("1 Ping Test")
    print("2 IP Info")
    print("3 Port Scan")
    print("4 Find Clean IP")
    print("5 Scan Range")
    print("6 Exit")

    c = input("Select: ")

    if c == "1":
        ip = input("IP: ")
        ping(ip)

    elif c == "2":
        ip = input("IP: ")
        ip_info(ip)

    elif c == "3":
        ip = input("IP: ")
        port_scan(ip)

    elif c == "4":
        base = input("Base IP (example 192.168.1): ")
        find_clean(base)

    elif c == "5":
        base = input("Base IP: ")
        start = int(input("Start: "))
        end = int(input("End: "))
        scan_range(base,start,end)

    elif c == "6":
        break
