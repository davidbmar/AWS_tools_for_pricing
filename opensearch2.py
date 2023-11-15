import subprocess
import json
import csv
import pprint

def list_domains():
        try:
             cmd = "aws opensearch list-domain-names"
             result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
             domain_data = json.loads(result.stdout)
             print("Raw domain data:", domain_data)  # Debug print
             if 'DomainNames' in domain_data:
                  domain_names = [domain['DomainName'] for domain in domain_data['DomainNames']]
                  return domain_names
             else:
                  print("No 'DomainNames' key in data")
                  return []
        except Exception as e:
             print("Error listing domains: {}".format(e))
             return []

def get_domain_details(domain_name):
        try:
             cmd = "aws opensearch describe-domain --domain-name {}".format(domain_name)
             result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
             return json.loads(result.stdout)['DomainStatus']
        except Exception as e:
             print("Error retrieving details for domain {}: {}".format(domain_name, e))
             return None

def extract_data(domain_details):
        extracted_data = []
        for detail in domain_details:
             if detail:
                 instance_type = detail['ClusterConfig']['InstanceType']
                 # Add other relevant fields here
                 extracted_data.append({'domain_name': detail['DomainName'], 'instance_type': instance_type})
        return extracted_data
def extract_data(domain_details):
        extracted_data = []
        for detail in domain_details:
            if detail:
               instance_type = detail['ClusterConfig']['InstanceType']
               volume_type = detail['EBSOptions']['VolumeType']
               volume_size = detail['EBSOptions']['VolumeSize']
               availability_zone_count = detail['ClusterConfig'].get('ZoneAwarenessConfig', {}).get('AvailabilityZoneCount', 'N/A')
               dedicated_master_count = detail['ClusterConfig'].get('DedicatedMasterCount', 'N/A') 
               multi_az_with_standby_enabled = detail['ClusterConfig'].get('MultiAZWithStandbyEnabled', False)
               ebs_enabled = detail['EBSOptions']['EBSEnabled']
               availability_zones = ", ".join(detail['VPCOptions'].get('AvailabilityZones', []))
   
               extracted_data.append({
                   'domain_name': detail['DomainName'],
                   'instance_type': instance_type,
                   'volume_type': volume_type,
                   'volume_size': volume_size,
                   'availability_zone_count': availability_zone_count,
                   'dedicated_master_count': dedicated_master_count,
                   'multi_az_with_standby_enabled': multi_az_with_standby_enabled,
                   'ebs_enabled': ebs_enabled,
                   'availability_zones': availability_zones
               })
        return extracted_data


def export_to_csv(data, filename='opensearch_domains.csv'):
        keys = data[0].keys()
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

domains = list_domains()
print("Domains: ", domains)

domain_details = [get_domain_details(domain) for domain in domains]
print("Domain Details: ", domain_details)

extracted_data = extract_data(domain_details)
print("Extracted Data: ", extracted_data)

export_to_csv(extracted_data)

