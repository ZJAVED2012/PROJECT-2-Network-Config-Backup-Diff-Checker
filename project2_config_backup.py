##############################################################
# Project 2: Network Config Backup + Diff Checker
# Simulation Mode (No real switches or routers required)
# Author: Zeeshan Javed
##############################################################

import os
import datetime
import difflib

# ----------------------------
# Simulation ON
# ----------------------------
simulation = True

# ----------------------------
# Device List
# ----------------------------
devices = [
    {"hostname": "Switch1", "IP": "192.168.1.10"},
    {"hostname": "Router1", "IP": "192.168.1.11"},
    {"hostname": "Firewall1", "IP": "192.168.1.12"},
]

# ----------------------------
# Simulated Configs for Testing
# ----------------------------
simulated_configs = {
    "Switch1": """
hostname Switch1
interface Fa0/1
 switchport mode access
 switchport access vlan 10
!
""",

    "Router1": """
hostname Router1
interface Gig0/1
 ip address 192.168.1.1 255.255.255.0
!
""",

    "Firewall1": """
hostname Firewall1
policy allow all
interface WAN
 security-level 100
!
"""
}

# ----------------------------
# Create backup directory
# ----------------------------
backup_folder = "backups"
if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

# ----------------------------
# Main Script
# ----------------------------
print("\nStarting Config Backup...\n")
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

for device in devices:
    hostname = device["hostname"]
    file_name = f"{backup_folder}/{hostname}_{timestamp}.txt"

    print(f"Backing up config from {hostname}...")

    # ----------------------------
    # Simulation Mode
    # ----------------------------
    if simulation:
        config_output = simulated_configs[hostname]
        print(f"SIMULATED CONFIG RECEIVED from {hostname}")
    else:
        config_output = "REAL DEVICE CONFIG (SSH REQUIRED)"

    # Save backup file
    with open(file_name, "w") as f:
        f.write(config_output)

    print(f" Config saved: {file_name}\n")


# ----------------------------
# DIFF CHECKER (Compare Latest 2 Backups)
# ----------------------------
print("\nChecking for config changes...\n")

for device in devices:
    hostname = device["hostname"]

    # List all backups for this device
    device_files = sorted([f for f in os.listdir(backup_folder) if hostname in f])

    if len(device_files) < 2:
        print(f" Not enough backups to compare for {hostname}")
        continue

    # Compare latest two configs
    old_file = f"{backup_folder}/{device_files[-2]}"
    new_file = f"{backup_folder}/{device_files[-1]}"

    with open(old_file) as f1, open(new_file) as f2:
        old_data = f1.readlines()
        new_data = f2.readlines()

    diff = difflib.unified_diff(
        old_data, new_data,
        fromfile=old_file,
        tofile=new_file,
        lineterm=""
    )

    diff_output = list(diff)

    if diff_output:
        print(f"\n CHANGES FOUND in {hostname}:\n")
        for line in diff_output:
            print(line)
    else:
        print(f"✔ No changes found in {hostname}")

print("\nProject 2 Completed Successfully! ")
