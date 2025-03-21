import paramiko
import sys
import json
from tabulate import tabulate

def create_table(json_output):
    # Create headers for the table
    headers = ["guest_id", "guest_type", "first_name", "last_name", "dob", "room_no", "start_time", "end_time"]
    # Iterate through JSON and create tuples
    table_data = [(user["guest_id"], user["guest_type"], user["first_name"], user["last_name"], user["dob"], user["guest_booking"][0]["room_no"], user["guest_booking"][0]["start_time"], user["guest_booking"][0]["end_time"]) for user in json_output]
    # Sort table
    table_data.sort(key=lambda tup: tup[5]) 
    # Show table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    

def ssh_connect(ip_address, guest_type_is, username, password):
    try:
        # Create an SSH client
        client = paramiko.SSHClient()
        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to the server
        client.connect(ip_address, username=username, password=password)
        print(f"Successfully connected to {ip_address}")
        # Execute the curl command
        command = f"curl -k 'https://vmxp.vikingship.local/VRC/MXP_RC.exe/Guest/?current_ship=true&showdatetime=true&guest_type={guest_type_is}'"
        stdin, stdout, stderr = client.exec_command(command)
        json_output=json.loads(stdout.read().decode())
        #output = json.dumps(json_output, indent=4)
        # Close the connection
        client.close()
        return json_output
    except Exception as e:
        print(f"Failed to connect to {ip_address}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python ssh_connect.py <IP_ADDRESS> <GUEST_TYPE> <USERNAME> <PASSWORD>")
        sys.exit(1)
    
    ip_address = sys.argv[1]
    guest_type_is = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    
    users_json = ssh_connect(ip_address, guest_type_is, username, password)
    create_table(users_json)