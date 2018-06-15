#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5
import boto3,botocore
session = boto3.session.Session(profile_name="saml")
ec2=session.resource('ec2')
instanceIDs=tuple(open('/Users/vgori/GoogleDrive/CengageLearning/Qualys/Qualys_Auth_Scan/exclude/Consolidated_Instance_Lists/PROD/REMAINING_PROD_instanceID', 'r'))
#instanceIDs=tuple(open('/Users/vgori/OneDriveBusiness/CengageLearning/Qualys/Qualys_Auth_Scan/exclude/Consolidated_Instance_Lists/QA/REMAINING_QA_instanceID', 'r'))
#instanceIDs=tuple(open('/Users/vgori/OneDriveBusiness/CengageLearning/Qualys/Qualys_Auth_Scan/exclude/Consolidated_Instance_Lists/DEV/REMAINING_DEV_instanceID', 'r'))
for i in instanceIDs:
	instance = ec2.Instance(str(i.strip()))
	try:
		print (instance.platform,instance.state['Name'],instance.id)
	except botocore.exceptions.ClientError as err:
		print (err)
	except AttributeError as err:
		print (err)
