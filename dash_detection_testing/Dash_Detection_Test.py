# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 07:46:39 2025

@author: JoshuaPaterson
"""

import subprocess
import time
from datetime import datetime

# IPv6 address of the Dash (include correct interface ID, like %12)
DASH_IP = "fe80::ae1d:dfff:fe40:58a7%5"
CHECK_INTERVAL = 5  # seconds
LOG_FILE = "dash_watchdog.log"

dash_online = None  # State tracker

def log_event(message, is_alert=False):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_msg = f"{timestamp} {message}"
    
    # Print to console
    if is_alert:
        print(f"\n=== {log_msg} ===\n")
    else:
        print(log_msg)
    
    # Save to file using UTF-8 encoding
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def ping_dash():
    try:
        result = subprocess.run(
            ["ping", "-n", "1", DASH_IP],
            capture_output=True, text=True, timeout=3
        )
        return "ms" in result.stdout
    except Exception as e:
        log_event(f"Ping error: {e}", is_alert=True)
        return False

def main():
    global dash_online
    log_event("🔍 Starting Dash watchdog...")

    while True:
        is_online = ping_dash()

        if dash_online is None:
            dash_online = is_online
            log_event("✅ Dash is ONLINE." if is_online else "❌ Dash is OFFLINE.", is_alert=True)

        elif is_online != dash_online:
            dash_online = is_online
            if is_online:
                log_event("✅ Dash turned ON.", is_alert=True)
            else:
                log_event("❌ Dash turned OFF.", is_alert=True)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()