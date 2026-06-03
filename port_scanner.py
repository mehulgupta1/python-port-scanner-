#!/usr/bin/env python3
"""
==============================================
  Port Scanner — by Eaglex
  GitHub: github.com/mehulgupta
  Tool: Scans open TCP ports on a target host
==============================================
"""

import socket
import threading
import sys
from datetime import datetime

# ── CONFIG ──────────────────────────────────
open_ports = []
lock = threading.Lock()
# ────────────────────────────────────────────


def scan_port(target_ip, port):
    """Try to connect to a port. If successful, it's open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # wait max 1 second per port
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            with lock:
                open_ports.append(port)
                # Try to get the service name for the port
                try:
                    service = socket.getservbyport(port, "tcp")
                except:
                    service = "unknown"
                print(f"  [OPEN]  Port {port:<6}  Service: {service}")
        sock.close()
    except socket.error:
        pass


def banner(target, start_port, end_port):
    print("=" * 50)
    print("       MEHUL'S PORT SCANNER")
    print("=" * 50)
    print(f"  Target   : {target}")
    print(f"  Ports    : {start_port} - {end_port}")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()


def resolve_host(host):
    """Convert hostname to IP address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[ERROR] Could not resolve host: {host}")
        sys.exit(1)


def main():
    # ── USER INPUT ───────────────────────────
    target = input("Enter target IP or hostname: ").strip()
    start_port = int(input("Start port [default 1]: ").strip() or 1)
    end_port   = int(input("End port   [default 1024]: ").strip() or 1024)
    # ─────────────────────────────────────────

    target_ip = resolve_host(target)
    banner(target_ip, start_port, end_port)

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

        # Limit concurrent threads to avoid overwhelming the system
        if len(threads) >= 100:
            for t in threads:
                t.join()
            threads = []

    # Wait for remaining threads
    for t in threads:
        t.join()

    print()
    print("=" * 50)
    print(f"  Scan complete. {len(open_ports)} open port(s) found.")
    print(f"  Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)


if __name__ == "__main__":
    main()


# ────────────────────────────────────────────────────────────
