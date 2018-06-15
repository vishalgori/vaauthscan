import boto3
session = boto3.session.Session(profile_name="saml")
#ec2=session.resource('ec2')
client = session.client('ec2')
#instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
instances = client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
print(instances)
instance_ids=[]
private_ips=[]
for i in range(0,len(instances['Reservations'])):
    instance_ids.append(instances['Reservations'][i]['Instances'][0]['InstanceId'])
    print("InstanceIDs: "+instance_ids)
    for j in range(0,len(instances['Reservations'][i]['Instances'][0]['NetworkInterfaces'])):
        private_ips.append(instances['Reservations'][i]['Instances'][0]['NetworkInterfaces'][j])


'''for i in instances:
  print(i.id,i.private_ip_address,i.tags)'''
'''for i in instances:
  for tag in i.tags:
    if(tag['Key']=='Name'):
      print (tag['Value'])'''
