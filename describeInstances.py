import boto3, json, os

def lambda_handler(event, context):
    account = os.environ['account'].upper()
    ec2_client = assume_role(account) #STS to assume account role for which we need to describe_instances()
    #ec2_client = boto3.client('ec2')
    ec2_info = ec2_client.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    #print ec2_info
    Product,InstanceID, PrivateIP, InstanceState, PublicDnsName, PublicIP = get_all_instance_info(ec2_info)
    sns_message = json.dumps([{'Product':GProduct,'InstanceID':InstanceID,'PrivateIP':PrivateIP,'InstanceState':InstanceState,'PublicDnsName':PublicDnsName,'PublicIP':PublicIP}])
    sns_client = boto3.client('sns')
    sns_arn = 'arn:aws:sns:us-east-1:1234:describeInstance'
    response = sns_client.publish(TargetArn=sns_arn, Message=sns_message)
    return sns_message, response

def assume_role(account):
    if account == "V": role_arn = "arn:aws:iam::1234:role/Dev-securityrole"
    elif account == "E2": role_arn = "arn:aws:iam::123:role/ADFS-ReadOnly"
    elif account == "A": role_arn = "arn:aws:iam::1232:role/ADFS-ReadOnly"
    elif account == "A2": role_arn = "arn:aws:iam::1234:role/ADFS-ReadOnly"
    elif account == "RD": role_arn = "arn:aws:iam::1234:role/ADFS-ReadOnly"
    elif account == "RD2": role_arn = "arn:aws:iam::1234:role/ADFS-ReadOnly"
    elif account == "LO": role_arn = "arn:aws:iam::1223:role/ADFS-ReadOnly"
    else: print ("Please select account names as one of the following: DEV/DEV2/QA/QA2/PROD/PROD2/LO") #Return this as message to slack

    # create an STS client object that represents a live connection to the
    # STS service
    sts_client = boto3.client('sts')

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    assumedRoleObject = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRoleSession1"
    )

    # From the response that contains the assumed role, get the temporary
    # credentials that can be used to make subsequent API calls
    credentials = assumedRoleObject['Credentials']

    # Use the temporary credentials that AssumeRole returns to make a
    # connection to Amazon S3
    ec2_client = boto3.client(
    'ec2',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken'],
    )
    return ec2_client

    '''resource = boto3.resource(
        's3',
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken'],
    )

    # Use the Amazon S3 resource object that is now configured with the
    # credentials to access your S3 buckets.
    for bucket in s3_resource.buckets.all():
        print(bucket.name)
        return bucket.name'''

def get_all_instance_info(ec2_info):

    Product = []
    InstanceID = []
    InstanceState = []
    PrivateIP = []
    PublicDnsName = []
    PublicIP = []
    n = len(ec2_info['Reservations'])

    #Extracting IP and product information for instances
    for i in range(0, n):
        try:
            for j in range(0, len(ec2_info['Reservations'][i]['Instances'][0]['Tags'])):
                if ec2_info['Reservations'][i]['Instances'][0]['Tags'][j]['Key'] == 'Product':
                    Product.append(ec2_info['Reservations'][i]['Instances'][0]['Tags'][j]['Value'])
                elif (ec2_info['Reservations'][i]['Instances'][0]['Tags'][j]['Key'] != 'Product' and j == len(
                        ec2_info['Reservations'][i]['Instances'][0]['Tags'])):
                    Product.append('NA')
        except IndexError:
            Product.append('NA')
        InstanceID.append(ec2_info['Reservations'][i]['Instances'][0]['InstanceId'])
        InstanceState.append(ec2_info['Reservations'][i]['Instances'][0]['State']['Name'])
        PublicDnsName.append(ec2_info['Reservations'][i]['Instances'][0]['PublicDnsName'])
        try:
            PrivateIP.append(
                ec2_info['Reservations'][i]['Instances'][0]['PrivateIpAddress'])
        except:
            PrivateIP.append('NA')
        try:
            PublicIP.append(
                ec2_info['Reservations'][i]['Instances'][0]['PublicIpAddress'])
        except KeyError:
            PublicIP.append('NA')

    #print (PublicIP)
    return Product,InstanceID,PrivateIP,InstanceState,PublicDnsName,PublicIP
