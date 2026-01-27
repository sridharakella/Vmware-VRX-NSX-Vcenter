#! /usr/local/Python_envs/Python3/bin/python3
'''
esxcli commands
################################################################################
Get Running VMs list     : esxcli vm process list
Shutdown Each running VM : esxcli vm process kill --type=soft --world-id={vm}
Enter Manitenance Mode   : esxcli system maintenanceMode set -e true
Shutdown ESXi Server     : esxcli system shutdown poweroff --reason=maintenance
################################################################################
'''
import time

import paramiko
from getpass import getpass
import re
try:
        vm_pass = getpass("Enter Password:")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='192.168.0.10', username='root', password=vm_pass)
        count = 0
        while count <2:
            print(f"\n{'#' * 50}\nChecking Running VMs")
            stdin, stdout, stderr = ssh_client.exec_command("esxcli vm process list")
            output = stdout.read().decode()
            print(output)
            world_ids = re.findall(r"World ID: (\d+)", output)
            if len(world_ids) == 0:
                print("All the VMs are down")
                time.sleep(2)

                print("Entering maintenance mode")
                maintenance_command = 'esxcli system maintenanceMode set -e true'
                stdin, stdout, stderr = ssh_client.exec_command(maintenance_command)
                time.sleep(5)

                print("Executing Shutdown")
                shutdown_command = 'esxcli system shutdown poweroff --reason=maintenance'
                stdin, stdout, stderr = ssh_client.exec_command(shutdown_command)
                stdin.close()
                break

            else:
                print(f"Running VM list: {world_ids}")
                print("Shutting down Each VM")
                for vm in world_ids:
                    print(f"Shutting down {vm}")
                    ssh_client.exec_command(f"esxcli vm process kill --type=soft --world-id={vm}")
                    time.sleep(2)
                count += 1
                if count == 2:
                    print("Exiting the loop without completing shutdown task")
except:
    print("ESXi not reachable")

print("Script Execution Completed")