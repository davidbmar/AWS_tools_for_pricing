#!/usr/bin/python3
# Import required modules
import boto3
import csv

# Initialize the EC2 client
ec2 = boto3.client('ec2')

def fetch_ec2_details():
    # Open CSV file for writing
    with open('running_ec2_instances.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Instance ID', 'Instance State', 'Instance Type', 'Monitoring Status', 'Security Groups']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Fetch the EC2 instance information
        response = ec2.describe_instances()

        # Loop through reservations and instances to collect details
        for reservation in response["Reservations"]:
                        for instance in reservation["Instances"]:
                            instance_id = instance["InstanceId"]
                            instance_state = instance["State"]["Name"]
                            instance_type = instance["InstanceType"]
                            monitoring_status = instance["Monitoring"]["State"]

                            # Fetching Security Group names
                            security_group_names = ', '.join([sg['GroupName'] for sg in instance["SecurityGroups"]])

                            # Fetching "Name" Tag
                            name_tag = next((tag['Value'] for tag in instance.get("Tags", []) if tag['Key'] == 'Name'), 'N/A')

                            # Check if the instance is running
                            if instance_state.lower() == 'running':
                                # Write to CSV
                                writer.writerow({'Name': name_tag,
                                            'Instance ID': instance_id,
                                            'Instance State': instance_state,
                                            'Instance Type': instance_type,
                                            'Monitoring Status': monitoring_status,
                                            'Security Groups': security_group_names})

if __name__ == "__main__":
        fetch_ec2_details()

